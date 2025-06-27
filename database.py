"""
Sistema de banco de dados para o bot CEPzinho
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from logperformance import LogPerformance


class Database:
    def __init__(self, db_path: str = "cepzinho.db"):
        """Inicializa a conexão com o banco de dados"""
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self):
        """Cria as tabelas necessárias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Tabela de consultas
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS queries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        user_name TEXT,
                        user_full_name TEXT,
                        query_type TEXT NOT NULL,
                        query_text TEXT NOT NULL,
                        result_data TEXT,
                        success BOOLEAN NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )

                # Tabela de usuários autorizados
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS authorized_users (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER UNIQUE NOT NULL,
                        user_name TEXT,
                        user_full_name TEXT,
                        role TEXT DEFAULT 'admin',
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )

                # Tabela de estatísticas
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS statistics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        total_queries INTEGER DEFAULT 0,
                        successful_queries INTEGER DEFAULT 0,
                        failed_queries INTEGER DEFAULT 0,
                        unique_users INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(date)
                    )
                """
                )

                conn.commit()
                LogPerformance().info("Tabelas do banco de dados criadas com sucesso")

        except Exception as e:
            LogPerformance().error(f"Erro ao criar tabelas: {e}")

    def add_query(
        self,
        user_id: int,
        user_name: str,
        user_full_name: str,
        query_type: str,
        query_text: str,
        result_data: Optional[Dict] = None,
        success: bool = True,
    ) -> bool:
        """Adiciona uma nova consulta ao banco de dados"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO queries (user_id, user_name, user_full_name, query_type, 
                                       query_text, result_data, success)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        user_id,
                        user_name,
                        user_full_name,
                        query_type,
                        query_text,
                        json.dumps(result_data) if result_data else None,
                        success,
                    ),
                )

                conn.commit()
                LogPerformance().info(
                    f"Consulta salva no banco: {query_type} - {query_text}"
                )
                return True

        except Exception as e:
            LogPerformance().error(f"Erro ao salvar consulta: {e}")
            return False

    def add_authorized_user(
        self, user_id: int, user_name: str, user_full_name: str, role: str = "admin"
    ) -> bool:
        """Adiciona um usuário autorizado"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT OR REPLACE INTO authorized_users (user_id, user_name, user_full_name, role)
                    VALUES (?, ?, ?, ?)
                """,
                    (user_id, user_name, user_full_name, role),
                )

                conn.commit()
                LogPerformance().info(f"Usuário autorizado adicionado: {user_id}")
                return True

        except Exception as e:
            LogPerformance().error(f"Erro ao adicionar usuário autorizado: {e}")
            return False

    def is_authorized(self, user_id: int) -> bool:
        """Verifica se um usuário está autorizado"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT id FROM authorized_users WHERE user_id = ?", (user_id,)
                )
                result = cursor.fetchone()

                return result is not None

        except Exception as e:
            LogPerformance().error(f"Erro ao verificar autorização: {e}")
            return False

    def get_recent_queries(self, limit: int = 50) -> List[Dict]:
        """Retorna as consultas mais recentes"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, user_name, user_full_name, query_type, query_text, 
                           result_data, success, created_at
                    FROM queries 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """,
                    (limit,),
                )

                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "user_id": row[0],
                            "user_name": row[1],
                            "user_full_name": row[2],
                            "query_type": row[3],
                            "query_text": row[4],
                            "result_data": json.loads(row[5]) if row[5] else None,
                            "success": bool(row[6]),
                            "created_at": row[7],
                        }
                    )

                return results

        except Exception as e:
            LogPerformance().error(f"Erro ao buscar consultas recentes: {e}")
            return []

    def get_user_queries(self, user_id: int, limit: int = 20) -> List[Dict]:
        """Retorna as consultas de um usuário específico"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT query_type, query_text, result_data, success, created_at
                    FROM queries 
                    WHERE user_id = ?
                    ORDER BY created_at DESC 
                    LIMIT ?
                """,
                    (user_id, limit),
                )

                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "query_type": row[0],
                            "query_text": row[1],
                            "result_data": json.loads(row[2]) if row[2] else None,
                            "success": bool(row[3]),
                            "created_at": row[4],
                        }
                    )

                return results

        except Exception as e:
            LogPerformance().error(f"Erro ao buscar consultas do usuário: {e}")
            return []

    def get_statistics(self, days: int = 7) -> Dict:
        """Retorna estatísticas dos últimos dias"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Total de consultas
                cursor.execute(
                    """
                    SELECT COUNT(*) as total, 
                           SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                           COUNT(DISTINCT user_id) as unique_users
                    FROM queries 
                    WHERE created_at >= datetime('now', '-{} days')
                """.format(
                        days
                    )
                )

                stats = cursor.fetchone()

                # Consultas por tipo
                cursor.execute(
                    """
                    SELECT query_type, COUNT(*) as count
                    FROM queries 
                    WHERE created_at >= datetime('now', '-{} days')
                    GROUP BY query_type
                """.format(
                        days
                    )
                )

                query_types = dict(cursor.fetchall())

                return {
                    "total_queries": stats[0] or 0,
                    "successful_queries": stats[1] or 0,
                    "failed_queries": (stats[0] or 0) - (stats[1] or 0),
                    "unique_users": stats[2] or 0,
                    "query_types": query_types,
                    "period_days": days,
                }

        except Exception as e:
            LogPerformance().error(f"Erro ao buscar estatísticas: {e}")
            return {}

    def get_authorized_users(self) -> List[Dict]:
        """Retorna lista de usuários autorizados"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, user_name, user_full_name, role, added_at
                    FROM authorized_users 
                    ORDER BY added_at DESC
                """
                )

                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "user_id": row[0],
                            "user_name": row[1],
                            "user_full_name": row[2],
                            "role": row[3],
                            "added_at": row[4],
                        }
                    )

                return results

        except Exception as e:
            LogPerformance().error(f"Erro ao buscar usuários autorizados: {e}")
            return []

    def get_summary_users(self) -> List[Dict]:
        """Retorna resumo de usuários"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT user_id, user_name, user_full_name
                    FROM queries
                    GROUP BY user_id
                    ORDER BY user_id DESC
                    """
                )

                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "user_id": row[0],
                            "user_name": row[1],
                            "user_full_name": row[2],
                        }
                    )
                return results
        except Exception as e:
            LogPerformance().error(f"Erro ao buscar resumo de usuários: {e}")
            return [{}]
