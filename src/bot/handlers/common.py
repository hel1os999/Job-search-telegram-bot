from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        "Job Search Bot\n\n"
        "/start — register\n"
        "/search — search vacancies\n"
        "/profile — profile for AI scoring\n"
        "/saved — saved vacancies\n"
        "/help — this help message"
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    import logging

    logging.getLogger(__name__).exception("Handler error", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Something went wrong. Please try again later or use /help."
        )


def register_common_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("help", help_command))
    app.add_error_handler(error_handler)
