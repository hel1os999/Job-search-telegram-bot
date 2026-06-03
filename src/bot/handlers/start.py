import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not user or not update.message:
        return

    container = context.application.bot_data["container"]
    async with container.session_factory() as session:
        repo = container.users(session)
        await repo.create_user(
            user.id,
            username=user.username,
            full_name=user.full_name,
        )
        await session.commit()

    logger.info("User registered: id=%s username=%s", user.id, user.username)
    await update.message.reply_text(
        "Hey! I'll help you find vacancies and score how well they match you.\n\n"
        "Commands:\n"
        "/search 'Vacancy Description' — search for vacancies\n"
        "/profile — set up your profile\n"
        "/saved — saved vacancies\n"
        "/help — help"
    )


def register_start_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start_command))
