import pytest
from schemas.user import UserProfileDTO
from schemas.vacancy import VacancyDTO
from services.matching.scorer import VacancyScorer


def _vacancy(external_id: str = "1", title: str = "Python Dev") -> VacancyDTO:
    return VacancyDTO(
        external_id=external_id,
        source="remotive",
        title=title,
        url=f"https://remotive.com/job/{external_id}",
    )


@pytest.fixture
def scorer_no_ai() -> VacancyScorer:
    from unittest.mock import MagicMock
    ai = MagicMock()
    ai.enabled = False
    return VacancyScorer(ai=ai)


@pytest.fixture
def profile() -> UserProfileDTO:
    return UserProfileDTO(
        desired_role="Python Developer",
        skills="Python, FastAPI",
        experience="2 years",
        location="Remote",
    )


@pytest.mark.asyncio
async def test_score_one_without_ai(scorer_no_ai, profile):
    vacancy = _vacancy()
    scored = await scorer_no_ai.score_one(profile, vacancy)
    assert scored.external_id == "1"
    assert scored.match_score == 50.0
    assert scored.ai_summary is None


@pytest.mark.asyncio
async def test_score_many_returns_sorted(scorer_no_ai, profile):
    vacancies = [_vacancy(str(i)) for i in range(5)]
    scored = await scorer_no_ai.score_many(profile, vacancies)
    scores = [v.match_score for v in scored]
    assert scores == sorted(scores, reverse=True)


@pytest.mark.asyncio
async def test_score_many_top_n(scorer_no_ai, profile):
    vacancies = [_vacancy(str(i)) for i in range(10)]
    scored = await scorer_no_ai.score_many(profile, vacancies, top_n=3)
    assert len(scored) == 3
