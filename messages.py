"""
Mensagens padrões do bot CEPzinho
"""

# Mensagem de boas-vindas
WELCOME_MESSAGE = """
🤖 Olá! Eu sou o CEPzinho, seu ajudante de endereços!

📍 Para buscar informações de um CEP, use o comando /cep seguido do número.

📝 Exemplos:
• /cep 01310-100
• /cep 01310100
• /cep 01310 100

🏠 Para buscar CEP por endereço, use /rua seguido do endereço.

💡 Use /help para ver todos os comandos disponíveis.

🔍 **Modo Inline:** Use @seu_bot_username + CEP ou endereço em qualquer chat!
"""

# Mensagem de ajuda
HELP_MESSAGE = """
📚 **Comandos disponíveis:**

/start - Inicia o bot
/help - Mostra esta mensagem de ajuda
/cep [número] - Busca endereço por CEP
/rua [endereço] - Busca CEP por endereço

📍 **Como usar /cep:**
/cep 01310-100
/cep 01310100
/cep 01310 100

🏠 **Como usar /rua:**
/rua Avenida Paulista, São Paulo
/rua Rua das Flores, 123, Centro
/rua Praça da Sé, São Paulo, SP

🔍 **Modo Inline:**
Use @seu_bot_username + CEP ou endereço em qualquer chat!

🔍 **Informações retornadas:**
• CEP
• Logradouro
• Bairro
• Cidade
• Estado
• DDD
• IBGE

❓ **Precisa de ajuda?** Entre em contato com o desenvolvedor.
"""

# Mensagem de formato inválido para CEP
INVALID_CEP_FORMAT_MESSAGE = """❌ Formato inválido! Envie um CEP válido com 8 dígitos.
Exemplos: /cep 01310-100, /cep 01310100, /cep 01310 100"""

# Mensagem de formato inválido para endereço
INVALID_ADDRESS_FORMAT_MESSAGE = """❌ Formato inválido! Use: /rua [endereço]
Exemplos: 
• /rua Avenida Paulista, São Paulo
• /rua Rua das Flores, 123, Centro
• /rua Praça da Sé, São Paulo, SP"""

# Mensagem de CEP não encontrado
CEP_NOT_FOUND_MESSAGE = "❌ CEP não encontrado. Verifique se o número está correto."

# Mensagem de endereço não encontrado
ADDRESS_NOT_FOUND_MESSAGE = "❌ Endereço não encontrado. Verifique se está correto."

# Mensagem de erro genérico
ERROR_MESSAGE = "❌ Erro ao buscar informações. Tente novamente mais tarde."

# Mensagem de CEP não configurado
TOKEN_NOT_CONFIGURED_MESSAGE = "❌ Token do Telegram não configurado no arquivo .env"

# Mensagem de uso incorreto do comando /cep
CEP_USAGE_MESSAGE = """📍 **Como usar o comando /cep:**

Envie: /cep [número do CEP]

📝 Exemplos:
• /cep 01310-100
• /cep 01310100
• /cep 01310 100

🔍 **Informações retornadas:**
• CEP formatado
• Logradouro
• Bairro
• Cidade
• Estado
• DDD
• Código IBGE
• Código SIAFI"""

# Mensagem de uso incorreto do comando /rua
RUA_USAGE_MESSAGE = """🏠 **Como usar o comando /rua:**

Envie: /rua [endereço completo]

📝 Exemplos:
• /rua Avenida Paulista, São Paulo
• /rua Rua das Flores, 123, Centro, São Paulo
• /rua Praça da Sé, São Paulo, SP

🔍 **Informações retornadas:**
• CEP
• Logradouro
• Bairro
• Cidade
• Estado"""

# Mensagens para modo inline
INLINE_QUERY_PLACEHOLDER = "Digite um CEP ou endereço..."
INLINE_RESULT_TITLE_CEP = "📍 CEP {cep}"
INLINE_RESULT_TITLE_ADDRESS = "🏠 {logradouro}"
INLINE_RESULT_DESCRIPTION_CEP = "{logradouro}, {bairro} - {cidade}/{uf}"
INLINE_RESULT_DESCRIPTION_ADDRESS = "CEP: {cep} - {cidade}/{uf}"
INLINE_NO_RESULTS = "Nenhum resultado encontrado"


def format_cep_response(cep_data: dict) -> str:
    """Formata a resposta da API do CEP"""
    if cep_data.get("erro"):
        return CEP_NOT_FOUND_MESSAGE

    response = f"""
📍 **Informações do CEP {cep_data.get('cep', 'N/A')}**

🏠 **Endereço:**
• Logradouro: {cep_data.get('logradouro', 'N/A')}
• Bairro: {cep_data.get('bairro', 'N/A')}
• Cidade: {cep_data.get('localidade', 'N/A')}
• Estado: {cep_data.get('uf', 'N/A')}

📞 **Informações adicionais:**
• DDD: {cep_data.get('ddd', 'N/A')}
• Código IBGE: {cep_data.get('ibge', 'N/A')}
• Código SIAFI: {cep_data.get('siafi', 'N/A')}
    """
    return response.strip()


def format_address_response(address_data: list) -> str:
    """Formata a resposta da busca por endereço"""
    if not address_data:
        return ADDRESS_NOT_FOUND_MESSAGE

    response = "🏠 **Endereços encontrados:**\n\n"

    for i, addr in enumerate(address_data[:5], 1):  # Limita a 5 resultados
        response += f"**{i}.** {addr.get('logradouro', 'N/A')}\n"
        response += f"   📍 CEP: {addr.get('cep', 'N/A')}\n"
        response += f"   🏘️ Bairro: {addr.get('bairro', 'N/A')}\n"
        response += f"   🏙️ Cidade: {addr.get('localidade', 'N/A')} - {addr.get('uf', 'N/A')}\n\n"

    if len(address_data) > 5:
        response += f"📝 *Mostrando 5 de {len(address_data)} resultados*"

    return response.strip()


def format_inline_cep_result(cep_data: dict) -> str:
    """Formata resultado inline para CEP"""
    if cep_data.get("erro"):
        return CEP_NOT_FOUND_MESSAGE

    return f"""📍 **CEP {cep_data.get('cep', 'N/A')}**
🏠 {cep_data.get('logradouro', 'N/A')}
🏘️ {cep_data.get('bairro', 'N/A')}
🏙️ {cep_data.get('localidade', 'N/A')} - {cep_data.get('uf', 'N/A')}"""


def format_inline_address_result(address_data: list) -> str:
    """Formata resultado inline para endereço"""
    if not address_data:
        return ADDRESS_NOT_FOUND_MESSAGE

    result = "🏠 **Endereços encontrados:**\n\n"

    for i, addr in enumerate(address_data[:3], 1):  # Limita a 3 para inline
        result += f"**{i}.** {addr.get('logradouro', 'N/A')}\n"
        result += f"📍 CEP: {addr.get('cep', 'N/A')}\n"
        result += f"🏙️ {addr.get('localidade', 'N/A')} - {addr.get('uf', 'N/A')}\n\n"

    if len(address_data) > 3:
        result += f"📝 *+{len(address_data) - 3} resultados*"

    return result.strip()
