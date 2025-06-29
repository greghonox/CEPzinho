"""
Mensagens padrões do bot CEPzinho
"""

WELCOME_MESSAGE = """
🤖 Olá! Eu sou o CEPzinho, seu ajudante de endereços!

📍 Para buscar informações de um CEP, use o comando /cep seguido do número.

📝 Exemplos:
• /cep 13183248
• /cep 36246200
• /cep 36246359

🏠 Para buscar CEP por endereço, use /rua seguido do endereço.

💡 Use /help para ver todos os comandos disponíveis.

🔍 **Modo Inline:** Use @cepzinhobot + CEP ou endereço em qualquer chat!
"""
CONTACT_MESSAGE = """
Se tiver alguma dúvida, entre em contato comigo no Telegram.

📞 TELEGRAM:

💡 @greghono
"""

HELP_MESSAGE = (
    """
📚 **Comandos disponíveis:**

/start - Inicia o bot
/help - Mostra esta mensagem de ajuda
/cep [número] - Busca endereço por CEP
/rua [endereço] - Busca CEP por endereço

📍 **Como usar /cep:**
/cep 13183248
/cep 36246200
/cep 36246359

🏠 **Como usar /rua:**
/rua Maria do Carmo Silva,  Santos dumont, MG
/rua rua maria , santos, MG
/rua Praça da Sé, São Paulo, SP

🔍 **Modo Inline:**
Use @cepzinhobot + CEP ou endereço em qualquer chat!

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
    + CONTACT_MESSAGE
)

INVALID_CEP_FORMAT_MESSAGE = (
    """❌ Formato inválido! Envie um CEP válido com 8 dígitos.
Exemplos: /cep 01310-100, /cep 01310100, /cep 01310 100"""
    + CONTACT_MESSAGE
)

INVALID_ADDRESS_FORMAT_MESSAGE = (
    """❌ Formato inválido! Use: /rua nome da rua, cidade, estado
Exemplos: 
• /rua Maria do Carmo Silva, Santos dumont, MG
• /rua rua maria , santos, MG
• /rua Praça da Sé, São Paulo, SP"""
    + CONTACT_MESSAGE
)

CEP_NOT_FOUND_MESSAGE = "❌ CEP não encontrado. Verifique se o número está correto."

ADDRESS_NOT_FOUND_MESSAGE = "❌ Endereço não encontrado. Verifique se está correto."

ERROR_MESSAGE = (
    "❌ Erro ao buscar informações. Tente novamente mais tarde."
    + "💡 Se aindanão conseguiu fazer a consulta e quiser chamar o desenvolvedor: "
    + CONTACT_MESSAGE
)

TOKEN_NOT_CONFIGURED_MESSAGE = "❌ Token do Telegram não configurado no arquivo .env"

CEP_USAGE_MESSAGE = """📍 **Como usar o comando /cep:**

Envie: /cep [número do CEP]

📝 Exemplos:
• /cep 13183248
• /cep 36246200
• /cep 36246359

🔍 **Informações retornadas:**
• CEP formatado
• Logradouro
• Bairro
• Cidade
• Estado
• DDD
• Código IBGE
• Código SIAFI"""

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

INLINE_QUERY_PLACEHOLDER = "Digite um CEP ou endereço..."
INLINE_RESULT_TITLE_CEP = "📍 CEP {cep}"
INLINE_RESULT_TITLE_ADDRESS = "🏠 {logradouro}"
INLINE_RESULT_DESCRIPTION_CEP = "{logradouro}, {bairro} - {cidade}/{uf}"
INLINE_RESULT_DESCRIPTION_ADDRESS = "CEP: {cep} - {cidade}/{uf}"
INLINE_NO_RESULTS = "Nenhum resultado encontrado"

NOT_AUTHORIZED_MESSAGE = "❌ Você não está autorizado a usar este comando."
ADMIN_HELP_MESSAGE = """
🔧 **Comandos de Administração:**

/stats - Mostra estatísticas do bot
/recent - Mostra consultas recentes
/users - Lista usuários autorizados
/adduser [user_id] - Adiciona usuário autorizado
/removeuser [user_id] - Remove usuário autorizado

📊 **Estatísticas disponíveis:**
• Total de consultas
• Consultas bem-sucedidas
• Usuários únicos
• Consultas por tipo
"""

STATS_MESSAGE = """
📊 **Estatísticas dos últimos {days} dias:**

🔍 **Consultas:**
• Total: {total_queries}
• Bem-sucedidas: {successful_queries}
• Falharam: {failed_queries}
• Taxa de sucesso: {success_rate:.1f}%

👥 **Usuários:**
• Únicos: {unique_users}

📈 **Por tipo:**
{query_types}

📅 Período: {days} dias
"""

RECENT_QUERIES_MESSAGE = """
🔍 Consultas Recentes:

{queries}

📝 Mostrando as {limit} consultas mais recentes
"""

USER_QUERIES_MESSAGE = """
👤 **Consultas do Usuário {user_id}:**

{queries}

📝 Mostrando as {limit} consultas mais recentes
"""

AUTHORIZED_USERS_MESSAGE = """
👥 **Usuários Autorizados:**

{users}

📝 Total: {count} usuários autorizados
"""

USER_ADDED_MESSAGE = "✅ Usuário {user_id} adicionado com sucesso!"
USER_REMOVED_MESSAGE = "✅ Usuário {user_id} removido com sucesso!"
USER_NOT_FOUND_MESSAGE = "❌ Usuário {user_id} não encontrado."


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


def format_stats_message(stats: dict) -> str:
    """Formata mensagem de estatísticas"""
    if not stats:
        return "❌ Erro ao buscar estatísticas."

    success_rate = 0
    if stats.get("total_queries", 0) > 0:
        success_rate = (
            stats.get("successful_queries", 0) / stats.get("total_queries", 1)
        ) * 100

    query_types_text = ""
    for query_type, count in stats.get("query_types", {}).items():
        query_types_text += f"• {query_type}: {count}\n"

    if not query_types_text:
        query_types_text = "👮🏿 Nenhuma consulta registrada\n"

    return STATS_MESSAGE.format(
        days=stats.get("period_days", 7),
        total_queries=stats.get("total_queries", 0),
        successful_queries=stats.get("successful_queries", 0),
        failed_queries=stats.get("failed_queries", 0),
        success_rate=success_rate,
        unique_users=stats.get("unique_users", 0),
        query_types=query_types_text,
    )


def format_recent_queries_message(queries: list, limit: int = 50) -> str:
    """Formata mensagem de consultas recentes"""
    if not queries:
        return "❌ Nenhuma consulta encontrada."

    queries_text = ""
    for query in queries[:limit]:
        status = "✅" if query.get("success") else "❌"
        queries_text += f"{status} **{query.get('user_name', 'N/A')}** - {query.get('query_type')}: {query.get('query_text')}\n"
        queries_text += f"   📅 {query.get('created_at')}\n\n"

    return RECENT_QUERIES_MESSAGE.format(queries=queries_text, limit=limit)


def format_authorized_users_message(users: list) -> str:
    """Formata mensagem de usuários autorizados"""
    if not users:
        return "❌ Nenhum usuário autorizado encontrado."

    users_text = ""
    for user in users:
        users_text += f"• **{user.get('user_name', 'N/A')}** ({user.get('user_full_name', 'N/A')})\n"
        users_text += f"  ID: {user.get('user_id')} | Role: {user.get('role')}\n"
        users_text += f"  📅 {user.get('added_at')}\n\n"

    return AUTHORIZED_USERS_MESSAGE.format(users=users_text, count=len(users))


def format_summary_users_message(users: list[dict]) -> str:
    """Formata mensagem de resumo de usuários"""
    if not users:
        return "❌ Nenhum usuário encontrado."

    users_text = "Usuarios que mais usaram o bot:\n"
    for user in users:
        users_text += f"👨🏿‍🔧 {user.get('user_name', 'N/A')} ({user.get('user_full_name', 'N/A')}) ID: {user.get('user_id')}\n"
    return users_text
