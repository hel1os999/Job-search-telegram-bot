from schemas.vacancy import ScoredVacancy, VacancyDTO
from utils.formatting import format_vacancy_card


def _make_vacancy(**kwargs) -> ScoredVacancy:
    defaults = dict(
        external_id="1",
        source="remotive",
        title="Python Developer",
        url="https://remotive.com/job/1",
        match_score=75.0,
    )
    defaults.update(kwargs)
    base = {k: v for k, v in defaults.items() if k in VacancyDTO.model_fields}
    score = defaults.get("match_score", 75.0)
    summary = defaults.get("ai_summary")
    return ScoredVacancy(**base, match_score=score, ai_summary=summary)


def test_format_card_contains_title():
    card = format_vacancy_card(_make_vacancy())
    assert "Python Developer" in card


def test_format_card_contains_score():
    card = format_vacancy_card(_make_vacancy(match_score=92.0))
    assert "92%" in card


def test_format_card_contains_url():
    card = format_vacancy_card(_make_vacancy())
    assert "https://remotive.com/job/1" in card


def test_format_card_with_company_and_salary():
    card = format_vacancy_card(_make_vacancy(company="Acme Corp", salary="$5000"))
    assert "Acme Corp" in card
    assert "$5000" in card


def test_format_card_with_ai_summary():
    card = format_vacancy_card(_make_vacancy(ai_summary="Great match for your skills."))
    assert "Great match" in card


def test_format_card_escapes_html():
    card = format_vacancy_card(_make_vacancy(title="Dev <Senior>"))
    assert "<Senior>" not in card
    assert "&lt;Senior&gt;" in card
