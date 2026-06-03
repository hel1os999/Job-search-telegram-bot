import logging

import httpx

from core.exceptions import JobSourceError
from schemas.vacancy import SearchFilters, VacancyDTO
from services.sources.base import JobSource
from core.config import settings

logger = logging.getLogger(__name__)

REMOTIVE_API_URL = "https://remotive.com/api"


class RemotiveSource(JobSource):
    name = "remotive"

    async def search(
        self,
        query: str,
        *,
        filters: SearchFilters | None = None,
        page: int = 0,
        per_page: int = 10,
    ) -> list[VacancyDTO]:
        params: dict[str, str | int] = {
            "search": query,
            "limit": per_page,
        }

        async with httpx.AsyncClient(base_url=settings.vacancy.remotive, timeout=30.0) as client:
            try:
                response = await client.get("/remote-jobs", params=params)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                logger.exception("Remotive API error")
                raise JobSourceError(str(exc)) from exc

        jobs = response.json().get("jobs", [])
        return [self._map_item(job) for job in jobs]

    def _map_item(self, job: dict) -> VacancyDTO:
        return VacancyDTO(
            external_id=str(job["id"]),
            source=self.name,
            title=job.get("title", ""),
            company=job.get("company_name"),
            url=job.get("url", ""),
            salary=job.get("salary") or None,
            location=job.get("candidate_required_location"),
            published_at=job.get("publication_date"),
        )
