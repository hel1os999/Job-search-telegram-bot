from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.vacancy import SavedVacancy
from schemas.vacancy import VacancyDTO


class VacancyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int, *, limit: int = 20) -> list[SavedVacancy]:
        result = await self.session.execute(
            select(SavedVacancy)
            .where(SavedVacancy.user_id == user_id)
            .order_by(SavedVacancy.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def save(
        self,
        user_id: int,
        vacancy: VacancyDTO,
        *,
        match_score: float | None = None,
        ai_summary: str | None = None,
    ) -> SavedVacancy:
        saved = SavedVacancy(
            user_id=user_id,
            external_id=vacancy.external_id,
            source=vacancy.source,
            title=vacancy.title,
            company=vacancy.company,
            url=vacancy.url,
            salary=vacancy.salary,
            description=vacancy.description,
            match_score=match_score,
            ai_summary=ai_summary,
        )
        self.session.add(saved)
        await self.session.commit()
        return saved

    async def is_saved(self, user_id: int, external_id: str, source: str) -> bool:
        result = await self.session.execute(
            select(SavedVacancy.id).where(
                SavedVacancy.user_id == user_id,
                SavedVacancy.external_id == external_id,
                SavedVacancy.source == source,
            )
        )
        return result.scalar_one_or_none() is not None
