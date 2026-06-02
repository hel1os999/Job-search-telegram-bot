from pydantic import BaseModel, Field


class SearchFilters(BaseModel):
    area: str | None = None
    salary_min: int | None = None
    experience: str | None = None
    employment: str | None = None
    schedule: str | None = None


class VacancyDTO(BaseModel):
    external_id: str
    source: str
    title: str
    company: str | None = None
    url: str
    salary: str | None = None
    description: str | None = None
    location: str | None = None
    published_at: str | None = None


class ScoredVacancy(VacancyDTO):
    match_score: float = Field(ge=0, le=100)
    ai_summary: str | None = None
