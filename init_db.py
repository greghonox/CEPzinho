#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do CEPzinho
"""

from database import Database
from logperformance import LogPerformance


def init_database():
    """Inicializa o banco de dados e adiciona usuário administrador"""
    print("🗄️  Inicializando banco de dados do CEPzinho...")

    try:
        # Cria o banco de dados
        db = Database()
        print("✅ Banco de dados criado com sucesso!")

        # Adiciona usuário administrador padrão
        # Substitua pelo seu user_id do Telegram
        admin_user_id = input(
            "Digite seu user_id do Telegram (ou pressione Enter para pular): "
        ).strip()

        if admin_user_id:
            try:
                admin_user_id = int(admin_user_id)
                success = db.add_authorized_user(
                    admin_user_id, "admin", "Administrador", "admin"
                )

                if success:
                    print(
                        f"✅ Usuário administrador {admin_user_id} adicionado com sucesso!"
                    )
                else:
                    print("❌ Erro ao adicionar usuário administrador.")

            except ValueError:
                print("❌ User ID deve ser um número válido.")
        else:
            print("⏭️  Pulando adição de usuário administrador.")

        # Mostra estatísticas iniciais
        stats = db.get_statistics(1)
        print(f"📊 Estatísticas iniciais: {stats.get('total_queries', 0)} consultas")

        # Mostra usuários autorizados
        users = db.get_authorized_users()
        print(f"👥 Usuários autorizados: {len(users)}")

        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("\n📋 Próximos passos:")
        print("1. Execute o bot: poetry run python main.py")
        print("2. Use /admin para ver comandos de administração")
        print("3. Use /adduser [user_id] para adicionar mais administradores")

    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        LogPerformance().error(f"Erro ao inicializar banco de dados: {e}")


def show_help():
    """Mostra ajuda sobre como obter o user_id"""
    print(
        """
🔍 **Como obter seu User ID no Telegram:**

1. **Método 1 - Via @userinfobot:**
   - Envie /start para @userinfobot
   - Ele retornará seu user_id

2. **Método 2 - Via @RawDataBot:**
   - Envie /start para @RawDataBot
   - Procure por "id" no resultado

3. **Método 3 - Via código:**
   - Envie uma mensagem para o bot
   - Verifique os logs do bot

📝 **Exemplo de user_id:** 123456789
"""
    )


if __name__ == "__main__":
    print("🤖 CEPzinho - Inicialização do Banco de Dados")
    print("=" * 50)

    choice = input("Deseja ver como obter seu user_id? (s/n): ").lower().strip()

    if choice in ["s", "sim", "y", "yes"]:
        show_help()
        print("\n" + "=" * 50)

    init_database()
