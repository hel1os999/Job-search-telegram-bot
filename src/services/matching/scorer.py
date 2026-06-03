from schemas.user import UserProfileDTO
from schemas.vacancy import ScoredVacancy, VacancyDTO
from services.ai.client import AIClient


class VacancyScorer:
    """Scores vacancies against user profile using a single AI batch request."""

    def __init__(self, ai: AIClient | None = None) -> None:
        self._ai = ai or AIClient()

    async def score_many(
        self,
        profile: UserProfileDTO,
        vacancies: list[VacancyDTO],
        *,
        top_n: int | None = None,
    ) -> list[ScoredVacancy]:
        if not vacancies:
            return []

        if not self._ai.enabled:
            scored = [ScoredVacancy(**v.model_dump(), match_score=50.0) for v in vacancies]
            return scored[:top_n] if top_n else scored

        vacancies_text = self._format_batch(vacancies)
        results = await self._ai.score_vacancies_batch(profile.to_context(), vacancies_text)

        scored: list[ScoredVacancy] = []
        for i, vacancy in enumerate(vacancies):
            item = results[i] if i < len(results) else {}
            scored.append(ScoredVacancy(
                **vacancy.model_dump(),
                match_score=float(item.get("score", 50)),
                ai_summary=item.get("summary"),
            ))

        scored.sort(key=lambda v: v.match_score, reverse=True)
        return scored[:top_n] if top_n else scored

    @staticmethod
    def _format_batch(vacancies: list[VacancyDTO]) -> str:
        parts = []
        for i, v in enumerate(vacancies, 1):
            lines = [f"[{i}] {v.title}"]
            if v.company:
                lines.append(f"Company: {v.company}")
            if v.salary:
                lines.append(f"Salary: {v.salary}")
            if v.location:
                lines.append(f"Location: {v.location}")
            parts.append("\n".join(lines))
        return "\n\n".join(parts)
