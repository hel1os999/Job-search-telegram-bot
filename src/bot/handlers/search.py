from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

from schemas.user import UserProfileDTO
from schemas.vacancy import ScoredVacancy
from utils.formatting import format_vacancy_card
from bot.keyboards.inline import vacancy_actions_keyboard


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    context.user_data["awaiting_search_query"] = True
    await update.message.reply_text(
        "Enter a search query (e.g. *Python developer remote*).\n"
        "AI can refine the query if your profile is filled in.",
        parse_mode="Markdown",
    )


async def search_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    if not context.user_data.pop("awaiting_search_query", False):
        return

    query = update.message.text.strip()
    user = update.effective_user
    if not user:
        return

    container = context.application.bot_data["container"]
    await update.message.reply_chat_action("typing")

    async with container.session_factory() as session:
        db_user = await container.users(session).get_by_telegram_id(user.id)
        profile = UserProfileDTO(
            skills=db_user.skills if db_user else None,
            experience=db_user.experience if db_user else None,
            desired_role=db_user.desired_role if db_user else None,
            desired_salary=db_user.desired_salary if db_user else None,
            location=db_user.location if db_user else None,
        )

    if container.ai_client.enabled and profile.to_context() != "No profile data":
        refined = await container.ai_client.refine_query(profile.to_context(), query)
        query = refined.get("query", query)
        explanation = refined.get("explanation")
        if explanation:
            await update.message.reply_text(explanation)

    vacancies = await container.job_search.search(query, per_page=5)

    if not vacancies:
        await update.message.reply_text("Nothing found. Try a different query.")
        return

    scored = await container.vacancy_scorer.score_many(profile, vacancies, top_n=5)

    context.user_data["last_vacancies"] = {
        f"{v.source}:{v.external_id}": v.model_dump() for v in scored
    }

    for vacancy in scored:
        await update.message.reply_text(
            format_vacancy_card(vacancy),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=vacancy_actions_keyboard(vacancy.external_id, vacancy.source),
        )


async def save_vacancy_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    _, source, external_id = query.data.split(":", 2)
    key = f"{source}:{external_id}"

    vacancy_data = (context.user_data.get("last_vacancies") or {}).get(key)
    if not vacancy_data:
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text("Could not find vacancy data. Please search again.")
        return

    user = update.effective_user
    if not user:
        return

    container = context.application.bot_data["container"]
    vacancy = ScoredVacancy(**vacancy_data)

    async with container.session_factory() as session:
        repo = container.vacancies(session)
        db_user = await container.users(session).get_by_telegram_id(user.id)
        if not db_user:
            await query.message.reply_text("Please use /start first.")
            return

        already = await repo.is_saved(db_user.id, external_id, source)
        if already:
            await query.edit_message_reply_markup(reply_markup=None)
            await query.message.reply_text("Already saved.")
            return

        await repo.save(
            db_user.id,
            vacancy,
            match_score=vacancy.match_score,
            ai_summary=vacancy.ai_summary,
        )
        await session.commit()

    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text(f"✅ Saved: {vacancy.title}")


def register_search_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_query_handler), group=1)
    app.add_handler(CallbackQueryHandler(save_vacancy_callback, pattern=r"^save:"))
