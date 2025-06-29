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
    NOT_AUTHORIZED_MESSAGE,
    ADMIN_HELP_MESSAGE,
    USER_ADDED_MESSAGE,
    USER_REMOVED_MESSAGE,
    USER_NOT_FOUND_MESSAGE,
    format_cep_response,
    format_address_response,
    format_inline_cep_result,
    format_stats_message,
    format_recent_queries_message,
    format_authorized_users_message,
    format_summary_users_message,
)
from config import (
    TELEGRAM_TOKEN,
    CEP_LENGTH,
    CEP_PATTERN,
    LOG_MESSAGES,
)
from database import Database


class CEPzinho:
    def __init__(self) -> None:
        LogPerformance().warning(LOG_MESSAGES["start"])
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.db = Database()
        self._setup_handlers()

    def _setup_handlers(self):
        """Configura os handlers do bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("cep", self.cep_command))
        self.app.add_handler(CommandHandler("rua", self.rua_command))

        self.app.add_handler(CommandHandler("admin", self.admin_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("recent", self.recent_command))
        self.app.add_handler(CommandHandler("users", self.users_command))
        self.app.add_handler(
            CommandHandler("summary_users", self.summary_users_command)
        )
        self.app.add_handler(CommandHandler("adduser", self.adduser_command))
        self.app.add_handler(CommandHandler("removeuser", self.removeuser_command))

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
        user_name = update.effective_user.username or "N/A"
        user_full_name = update.effective_user.full_name or "N/A"

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

            # Salva no banco de dados
            success = not cep_data.get("erro")
            self.db.add_query(
                user_id, user_name, user_full_name, "cep", cep_input, cep_data, success
            )

            LogPerformance().info(
                LOG_MESSAGES["cep_processed"].format(cep=cep, user_id=user_id)
            )

        except Exception as e:
            LogPerformance().error(
                LOG_MESSAGES["cep_error"].format(cep=cep, error=str(e))
            )
            await update.message.reply_text(ERROR_MESSAGE)

            # Salva erro no banco de dados
            self.db.add_query(
                user_id, user_name, user_full_name, "cep", cep_input, None, False
            )

    async def rua_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /rua"""
        user_id = update.effective_user.id
        user_name = update.effective_user.username or "N/A"
        user_full_name = update.effective_user.full_name or "N/A"

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

            success = len(address_data) > 0
            self.db.add_query(
                user_id,
                user_name,
                user_full_name,
                "rua",
                address_input,
                {"results": address_data},
                success,
            )

            LogPerformance().info(
                f"Endereço '{address_input}' processado para usuário {user_id}"
            )

        except Exception as e:
            LogPerformance().error(
                f"Erro ao processar endereço '{address_input}': {str(e)}"
            )
            await update.message.reply_text(ERROR_MESSAGE)

            self.db.add_query(
                user_id, user_name, user_full_name, "rua", address_input, None, False
            )

    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /admin"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        await update.message.reply_text(ADMIN_HELP_MESSAGE.strip())

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /stats"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        try:
            stats = self.db.get_statistics(7)  # Últimos 7 dias
            response = format_stats_message(stats)
            await update.message.reply_text(response)
        except Exception as e:
            LogPerformance().error(f"Erro ao buscar estatísticas: {e}")
            await update.message.reply_text("❌ Erro ao buscar estatísticas.")

    async def summary_users_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handler para o comando /summary"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        try:
            users = self.db.get_summary_users()
            response = format_summary_users_message(users)
            await update.message.reply_text(response)
        except Exception as e:
            LogPerformance().error(f"Erro ao buscar resumo de usuários: {e}")
            await update.message.reply_text("❌ Erro ao buscar resumo de usuários.")

    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /recent"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        try:
            queries = self.db.get_recent_queries(20)  # Últimas 20 consultas
            response = format_recent_queries_message(queries, 20)
            await update.message.reply_text(response)
        except Exception as e:
            LogPerformance().error(f"Erro ao buscar consultas recentes: {e}")
            await update.message.reply_text("❌ Erro ao buscar consultas recentes.")

    async def users_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /users"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        try:
            users = self.db.get_authorized_users()
            response = format_authorized_users_message(users)
            await update.message.reply_text(response)
        except Exception as e:
            LogPerformance().error(f"Erro ao buscar usuários autorizados: {e}")
            await update.message.reply_text("❌ Erro ao buscar usuários autorizados.")

    async def adduser_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para o comando /adduser"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        if not context.args:
            await update.message.reply_text("❌ Use: /adduser [user_id]")
            return

        try:
            new_user_id = int(context.args[0])
            user_name = update.effective_user.username or "N/A"
            user_full_name = update.effective_user.full_name or "N/A"

            success = self.db.add_authorized_user(
                new_user_id, user_name, user_full_name
            )

            if success:
                await update.message.reply_text(
                    USER_ADDED_MESSAGE.format(user_id=new_user_id)
                )
            else:
                await update.message.reply_text("❌ Erro ao adicionar usuário.")
        except ValueError:
            await update.message.reply_text("❌ ID do usuário deve ser um número.")
        except Exception as e:
            LogPerformance().error(f"Erro ao adicionar usuário: {e}")
            await update.message.reply_text("❌ Erro ao adicionar usuário.")

    async def removeuser_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """Handler para o comando /removeuser"""
        user_id = update.effective_user.id

        if not self.db.is_authorized(user_id):
            await update.message.reply_text(NOT_AUTHORIZED_MESSAGE)
            return

        if not context.args:
            await update.message.reply_text("❌ Use: /removeuser [user_id]")
            return

        try:
            remove_user_id = int(context.args[0])

            # Implementar remoção no banco de dados
            # Por enquanto, apenas confirma
            await update.message.reply_text(
                USER_REMOVED_MESSAGE.format(user_id=remove_user_id)
            )
        except ValueError:
            await update.message.reply_text("❌ ID do usuário deve ser um número.")
        except Exception as e:
            LogPerformance().error(f"Erro ao remover usuário: {e}")
            await update.message.reply_text("❌ Erro ao remover usuário.")

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

                    self.db.add_query(
                        user_id, name, full_name, "inline_cep", query, cep_data, True
                    )
            except Exception as e:
                LogPerformance().error(f"Erro na consulta inline CEP: {e}")
                self.db.add_query(
                    user_id, name, full_name, "inline_cep", query, None, False
                )

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

                    self.db.add_query(
                        user_id,
                        name,
                        full_name,
                        "inline_address",
                        query,
                        {"results": address_data},
                        True,
                    )
            except Exception as e:
                LogPerformance().error(f"Erro na consulta inline endereço: {e}")
                self.db.add_query(
                    user_id, name, full_name, "inline_address", query, None, False
                )

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

    def run(self) -> None:
        """Inicia o bot"""
        LogPerformance().info(LOG_MESSAGES["bot_started"])
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    bot = CEPzinho()
    bot.run()
