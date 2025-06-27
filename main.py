from logperformance import LogPerformance
from cep import Cep
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    ContextTypes,
)
import re
from messages import (
    WELCOME_MESSAGE,
    HELP_MESSAGE,
    INVALID_CEP_FORMAT_MESSAGE,
    INVALID_ADDRESS_FORMAT_MESSAGE,
    ERROR_MESSAGE,
    CEP_USAGE_MESSAGE,
    RUA_USAGE_MESSAGE,
    INLINE_QUERY_PLACEHOLDER,
    INLINE_RESULT_TITLE_CEP,
    INLINE_RESULT_TITLE_ADDRESS,
    INLINE_RESULT_DESCRIPTION_CEP,
    INLINE_RESULT_DESCRIPTION_ADDRESS,
    INLINE_NO_RESULTS,
    format_cep_response,
    format_address_response,
    format_inline_cep_result,
)
from config import (
    TELEGRAM_TOKEN,
    CEP_LENGTH,
    CEP_PATTERN,
    LOG_MESSAGES,
)


class CEPzinho:
    def __init__(self) -> None:
        LogPerformance().warning(LOG_MESSAGES["start"])
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self._setup_handlers()

    def _setup_handlers(self):
        """Configura os handlers do bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("cep", self.cep_command))
        self.app.add_handler(CommandHandler("rua", self.rua_command))
        self.app.add_handler(InlineQueryHandler(self.inline_query))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /start"""
        await update.message.reply_text(WELCOME_MESSAGE.strip())
        user_id = update.effective_user.id
        LogPerformance().info(LOG_MESSAGES["user_started"].format(user_id=user_id))

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /help"""
        await update.message.reply_text(HELP_MESSAGE.strip())
        user_id = update.effective_user.id
        LogPerformance().info(LOG_MESSAGES["user_help"].format(user_id=user_id))

    async def cep_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /cep"""
        user_id = update.effective_user.id

        if not context.args:
            await update.message.reply_text(CEP_USAGE_MESSAGE.strip())
            return

        cep_input = " ".join(context.args)

        LogPerformance().info(
            LOG_MESSAGES["user_message"].format(
                user_id=user_id, message=f"/cep {cep_input}"
            )
        )

        cep = self._extract_cep(cep_input)

        if not cep:
            await update.message.reply_text(INVALID_CEP_FORMAT_MESSAGE)
            return

        try:
            cep_obj = Cep(cep)
            cep_data = cep_obj.get_cep()

            response = format_cep_response(cep_data)
            await update.message.reply_text(response)

            LogPerformance().info(
                LOG_MESSAGES["cep_processed"].format(cep=cep, user_id=user_id)
            )

        except Exception as e:
            LogPerformance().error(
                LOG_MESSAGES["cep_error"].format(cep=cep, error=str(e))
            )
            await update.message.reply_text(ERROR_MESSAGE)

    async def rua_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /rua"""
        user_id = update.effective_user.id

        if not context.args:
            await update.message.reply_text(RUA_USAGE_MESSAGE.strip())
            return

        address_input = " ".join(context.args)

        LogPerformance().info(
            LOG_MESSAGES["user_message"].format(
                user_id=user_id, message=f"/rua {address_input}"
            )
        )

        try:
            address_info = self._parse_address(address_input)

            if not address_info:
                await update.message.reply_text(INVALID_ADDRESS_FORMAT_MESSAGE)
                return

            cep_obj = Cep()
            address_data = cep_obj.search_address(
                address_info["uf"], address_info["cidade"], address_info["logradouro"]
            )

            response = format_address_response(address_data)
            await update.message.reply_text(response)

            LogPerformance().info(
                f"Endereço '{address_input}' processado para usuário {user_id}"
            )

        except Exception as e:
            LogPerformance().error(
                f"Erro ao processar endereço '{address_input}': {str(e)}"
            )
            await update.message.reply_text(ERROR_MESSAGE)

    async def inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para consultas inline"""
        query = update.inline_query.query.strip()
        user_id = update.inline_query.from_user.id
        full_name = update.inline_query.from_user.full_name
        name = update.inline_query.from_user.name

        if not query:
            results = [
                InlineQueryResultArticle(
                    id="placeholder",
                    title="Digite um CEP ou endereço...",
                    description=INLINE_QUERY_PLACEHOLDER,
                    input_message_content=InputTextMessageContent(
                        "Digite um CEP (ex: 01310-100) ou endereço (ex: Avenida Paulista, São Paulo, SP)"
                    ),
                )
            ]
            await update.inline_query.answer(results)
            return

        LogPerformance().info(
            f"Consulta inline de usuário {name} {full_name} {user_id}: {query}"
        )

        results = []

        cep = self._extract_cep(query)
        if cep:
            try:
                cep_obj = Cep(cep)
                cep_data = cep_obj.get_cep()

                if not cep_data.get("erro"):
                    title = INLINE_RESULT_TITLE_CEP.format(cep=cep_data.get("cep"))
                    description = INLINE_RESULT_DESCRIPTION_CEP.format(
                        logradouro=cep_data.get("logradouro", "N/A"),
                        bairro=cep_data.get("bairro", "N/A"),
                        cidade=cep_data.get("localidade", "N/A"),
                        uf=cep_data.get("uf", "N/A"),
                    )
                    content = format_inline_cep_result(cep_data)

                    results.append(
                        InlineQueryResultArticle(
                            id=f"cep_{cep}",
                            title=title,
                            description=description,
                            input_message_content=InputTextMessageContent(content),
                        )
                    )
            except Exception as e:
                LogPerformance().error(f"Erro na consulta inline CEP: {e}")

        address_info = self._parse_address(query)
        if address_info:
            try:
                cep_obj = Cep()
                address_data = cep_obj.search_address(
                    address_info["uf"],
                    address_info["cidade"],
                    address_info["logradouro"],
                )

                if address_data:
                    for i, addr in enumerate(address_data[:3]):
                        title = INLINE_RESULT_TITLE_ADDRESS.format(
                            logradouro=addr.get("logradouro", "N/A")
                        )
                        description = INLINE_RESULT_DESCRIPTION_ADDRESS.format(
                            cep=addr.get("cep", "N/A"),
                            cidade=addr.get("localidade", "N/A"),
                            uf=addr.get("uf", "N/A"),
                        )
                        content = f"📍 **CEP {addr.get('cep', 'N/A')}**\n🏠 {addr.get('logradouro', 'N/A')}\n🏙️ {addr.get('localidade', 'N/A')} - {addr.get('uf', 'N/A')}"

                        results.append(
                            InlineQueryResultArticle(
                                id=f"addr_{i}_{addr.get('cep', '')}",
                                title=title,
                                description=description,
                                input_message_content=InputTextMessageContent(content),
                            )
                        )
            except Exception as e:
                LogPerformance().error(f"Erro na consulta inline endereço: {e}")

        if not results:
            results = [
                InlineQueryResultArticle(
                    id="no_results",
                    title="Nenhum resultado encontrado",
                    description=INLINE_NO_RESULTS,
                    input_message_content=InputTextMessageContent(
                        f"Não foi possível encontrar informações para: {query}"
                    ),
                )
            ]

        await update.inline_query.answer(results)

    def _extract_cep(self, text: str) -> str:
        """Extrai o CEP do texto da mensagem"""
        cep_clean = re.sub(CEP_PATTERN, "", text)

        if len(cep_clean) == CEP_LENGTH:
            return cep_clean

        return None

    def _parse_address(self, text: str) -> dict:
        """Extrai informações do endereço (UF, cidade, logradouro)"""
        parts = text.split(",")

        if len(parts) < 2:
            return None

        uf = parts[-1].strip().upper()

        cidade = parts[-2].strip()

        logradouro = ",".join(parts[:-2]).strip()

        if not uf or not cidade or not logradouro:
            return None

        return {"uf": uf, "cidade": cidade, "logradouro": logradouro}

    def run(self):
        """Inicia o bot"""
        LogPerformance().info(LOG_MESSAGES["bot_started"])
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = CEPzinho()
    bot.run()
