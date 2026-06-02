from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.search_query import SavedSearch


class SearchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_user(self, user_id: int) -> list[SavedSearch]:
        result = await self.session.execute(
            select(SavedSearch)
            .where(SavedSearch.user_id == user_id)
            .order_by(SavedSearch.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self,
        user_id: int,
        query: str,
        *,
        name: str | None = None,
        filters_json: str | None = None,
    ) -> SavedSearch:
        search = SavedSearch(
            user_id=user_id,
            query=query,
            name=name,
            filters_json=filters_json,
        )
        self.session.add(search)
        await self.session.commit()
        return search

    async def delete(self, search_id: int, user_id: int) -> bool:
        result = await self.session.execute(
            select(SavedSearch).where(
                SavedSearch.id == search_id,
                SavedSearch.user_id == user_id,
            )
        )
        search = result.scalar_one_or_none()
        if not search:
            return False
        await self.session.delete(search)
        await self.session.commit()
        return True
