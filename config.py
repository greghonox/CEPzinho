"""
Configurações do bot CEPzinho
"""

import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

CEP_API_URL = "https://viacep.com.br/ws/{cep}/json/"

LOG_LEVEL = "INFO"

CEP_LENGTH = 8
CEP_PATTERN = r"[^\d]"

LOG_MESSAGES = {
    "start": "Iniciando o programa",
    "bot_started": "Bot iniciado e aguardando mensagens...",
    "user_started": "Usuário {user_id} iniciou o bot",
    "user_help": "Usuário {user_id} solicitou ajuda",
    "user_message": "Usuário {user_id} enviou: {message}",
    "cep_processed": "CEP {cep} processado com sucesso para usuário {user_id}",
    "cep_error": "Erro ao processar CEP {cep}: {error}",
    "address_processed": "Endereço '{address}' processado para usuário {user_id}",
    "address_error": "Erro ao processar endereço '{address}': {error}",
    "inline_query": "Consulta inline de usuário {user_id}: {query}",
    "inline_cep_error": "Erro na consulta inline CEP: {error}",
    "inline_address_error": "Erro na consulta inline endereço: {error}",
    "token_error": "Token do Telegram não encontrado no arquivo .env",
}
