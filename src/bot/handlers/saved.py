import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from utils.formatting import format_saved_vacancy

logger = logging.getLogger(__name__)


async def saved_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    user = update.effective_user
    if not user:
        return

    container = context.application.bot_data["container"]
    async with container.session_factory() as session:
        db_user = await container.users(session).get_by_telegram_id(user.id)
        if not db_user:
            await update.message.reply_text("Please use /start first.")
            return
        saved = await container.vacancies(session).list_for_user(db_user.id)

    logger.info("Listing saved vacancies: user_id=%s count=%d", user.id, len(saved))
    if not saved:
        await update.message.reply_text("No saved vacancies yet.")
        return

    for item in saved:
        await update.message.reply_text(
            format_saved_vacancy(item),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )


def register_saved_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("saved", saved_command))
