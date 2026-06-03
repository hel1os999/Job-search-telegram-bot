import pytest
from schemas.user import UserProfileDTO
from schemas.vacancy import ScoredVacancy, VacancyDTO


# --- UserProfileDTO ---

def test_profile_context_empty():
    profile = UserProfileDTO()
    assert profile.to_context() == "No profile data"


def test_profile_context_filled():
    profile = UserProfileDTO(desired_role="Backend Developer", skills="Python, FastAPI")
    ctx = profile.to_context()
    assert "Backend Developer" in ctx
    assert "Python" in ctx


def test_profile_context_all_fields():
    profile = UserProfileDTO(
        desired_role="Python Developer",
        skills="Python, SQLAlchemy",
        experience="3 years",
        desired_salary=150000,
        location="Remote",
    )
    ctx = profile.to_context()
    assert "Python Developer" in ctx
    assert "SQLAlchemy" in ctx
    assert "3 years" in ctx
    assert "150000" in ctx
    assert "Remote" in ctx


def test_profile_context_partial():
    profile = UserProfileDTO(skills="Go, Rust")
    ctx = profile.to_context()
    assert "Go, Rust" in ctx
    assert ctx != "No profile data"


# --- VacancyDTO / ScoredVacancy ---

def test_vacancy_dto_required_fields():
    v = VacancyDTO(
        external_id="123",
        source="remotive",
        title="Python Dev",
        url="https://example.com/job/123",
    )
    assert v.external_id == "123"
    assert v.company is None
    assert v.salary is None


def test_scored_vacancy_score_bounds():
    base = VacancyDTO(
        external_id="1",
        source="remotive",
        title="Dev",
        url="https://example.com",
    )
    scored = ScoredVacancy(**base.model_dump(), match_score=85.0)
    assert scored.match_score == 85.0


def test_scored_vacancy_score_validation():
    base = VacancyDTO(
        external_id="1",
        source="remotive",
        title="Dev",
        url="https://example.com",
    )
    with pytest.raises(Exception):
        ScoredVacancy(**base.model_dump(), match_score=150.0)
