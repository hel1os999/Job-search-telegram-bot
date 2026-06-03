from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from services.ai.profile_parser import ProfileParser

import logging

log = logging.getLogger(__name__)

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    context.user_data["awaiting_profile_text"] = True
    print(context.user_data["awaiting_profile_text"])
    await update.message.reply_text(
        "Describe yourself in free text: skills, experience, desired role, salary, location.\n"
        "AI will extract the data and save your profile."
    )


async def profile_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("HIT profile_text_handler")
    if not update.message or not update.message.text:
        return
    if not context.user_data.pop("awaiting_profile_text", False):
        return

    log.info(f"Message from user:{update.message.text}")

    user = update.effective_user
    if not user:
        return

    log.info(f"Telegram user {user}")

    container = context.application.bot_data["container"]
    parser = ProfileParser(container.ai_client)
    profile = await parser.parse(update.message.text)

    async with container.session_factory() as session:
        repo = container.users(session)
        
        await repo.update_profile(
            user=await repo.get_by_telegram_id(user.id),
            skills=profile.skills,
            experience=profile.experience,
            desired_role=profile.desired_role,
            desired_salary=profile.desired_salary,
            location=profile.location,
        )
        await session.commit()

    await update.message.reply_text(
        "Profile saved:\n\n" + profile.to_context()
    )


def register_profile_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, profile_text_handler), group=2)
