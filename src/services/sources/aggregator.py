from schemas.vacancy import SearchFilters, VacancyDTO
from services.sources.base import JobSource
from services.sources.remotive import RemotiveSource


class JobSearchAggregator:
    """Runs search across all registered job sources."""

    def __init__(self, sources: list[JobSource] | None = None) -> None:
        self._sources = sources or [RemotiveSource()]

    async def search(
        self,
        query: str,
        *,
        filters: SearchFilters | None = None,
        page: int = 0,
        per_page: int = 10,
    ) -> list[VacancyDTO]:
        results: list[VacancyDTO] = []
        for source in self._sources:
            batch = await source.search(
                query,
                filters=filters,
                page=page,
                per_page=per_page,
            )
            results.extend(batch)
        return results
