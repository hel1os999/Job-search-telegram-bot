from abc import ABC, abstractmethod

from schemas.vacancy import SearchFilters, VacancyDTO


class JobSource(ABC):
    name: str

    @abstractmethod
    async def search(
        self,
        query: str,
        *,
        filters: SearchFilters | None = None,
        page: int = 0,
        per_page: int = 10,
    ) -> list[VacancyDTO]:
        ...
