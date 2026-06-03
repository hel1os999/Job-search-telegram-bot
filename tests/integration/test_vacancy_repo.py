import pytest
from db.repositories.user_repo import UserRepository
from db.repositories.vacancy_repo import VacancyRepository
from schemas.vacancy import VacancyDTO


def _dto(external_id: str = "42") -> VacancyDTO:
    return VacancyDTO(
        external_id=external_id,
        source="remotive",
        title="Python Developer",
        company="Acme",
        url=f"https://remotive.com/job/{external_id}",
        salary="$5000",
    )


@pytest.mark.asyncio
async def test_save_and_list(db_session):
    user = await UserRepository(db_session).get_or_create(1, username="u")
    await db_session.commit()

    repo = VacancyRepository(db_session)
    await repo.save(user.id, _dto("1"), match_score=80.0, ai_summary="Good fit.")
    await repo.save(user.id, _dto("2"), match_score=60.0)
    await db_session.commit()

    saved = await repo.list_for_user(user.id)
    assert len(saved) == 2


@pytest.mark.asyncio
async def test_is_saved_true(db_session):
    user = await UserRepository(db_session).get_or_create(2, username="u")
    await db_session.commit()

    repo = VacancyRepository(db_session)
    await repo.save(user.id, _dto("99"))
    await db_session.commit()

    assert await repo.is_saved(user.id, "99", "remotive") is True


@pytest.mark.asyncio
async def test_is_saved_false(db_session):
    user = await UserRepository(db_session).get_or_create(3, username="u")
    await db_session.commit()

    repo = VacancyRepository(db_session)
    assert await repo.is_saved(user.id, "999", "remotive") is False


@pytest.mark.asyncio
async def test_save_stores_score_and_summary(db_session):
    user = await UserRepository(db_session).get_or_create(4, username="u")
    await db_session.commit()

    repo = VacancyRepository(db_session)
    await repo.save(user.id, _dto("7"), match_score=95.0, ai_summary="Perfect.")
    await db_session.commit()

    saved = await repo.list_for_user(user.id)
    assert saved[0].match_score == 95.0
    assert saved[0].ai_summary == "Perfect."
