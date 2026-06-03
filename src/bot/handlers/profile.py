from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from services.ai.profile_parser import ProfileParser

import logging

logger = logging.getLogger(__name__)

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    context.user_data["awaiting_profile_text"] = True
    logger.info("Profile setup started: user_id=%s", update.effective_user.id if update.effective_user else "?")
    await update.message.reply_text(
        "Describe yourself in free text: skills, experience, desired role, salary, location.\n"
        "AI will extract the data and save your profile."
    )


async def profile_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    if not context.user_data.pop("awaiting_profile_text", False):
        return

    user = update.effective_user
    if not user:
        return

    logger.info("Profile text received: user_id=%s", user.id)

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

    logger.info("Profile saved: user_id=%s role=%s", user.id, profile.desired_role)
    await update.message.reply_text(
        "Profile saved:\n\n" + profile.to_context()
    )


def register_profile_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, profile_text_handler), group=2)
