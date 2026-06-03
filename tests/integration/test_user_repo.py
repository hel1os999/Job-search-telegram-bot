import pytest
from db.repositories.user_repo import UserRepository


@pytest.mark.asyncio
async def test_get_or_create_new_user(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_or_create(123456, username="testuser", full_name="Test User")
    await db_session.commit()

    assert user.telegram_id == 123456
    assert user.username == "testuser"
    assert user.full_name == "Test User"


@pytest.mark.asyncio
async def test_get_or_create_existing_user(db_session):
    repo = UserRepository(db_session)
    user1 = await repo.get_or_create(111, username="old_name")
    await db_session.commit()

    user2 = await repo.get_or_create(111, username="new_name")
    await db_session.commit()

    assert user1.id == user2.id
    assert user2.username == "new_name"


@pytest.mark.asyncio
async def test_get_by_telegram_id_not_found(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_by_telegram_id(999999)
    assert user is None


@pytest.mark.asyncio
async def test_update_profile(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_or_create(222, username="user")
    await db_session.commit()

    updated = await repo.update_profile(
        user,
        skills="Python, FastAPI",
        desired_role="Backend Developer",
        desired_salary=120000,
        location="Remote",
    )
    await db_session.commit()

    assert updated.skills == "Python, FastAPI"
    assert updated.desired_role == "Backend Developer"
    assert updated.desired_salary == 120000
    assert updated.location == "Remote"


@pytest.mark.asyncio
async def test_update_profile_partial(db_session):
    repo = UserRepository(db_session)
    user = await repo.get_or_create(333, username="user")
    await repo.update_profile(user, skills="Go", desired_role="Go Developer")
    await db_session.commit()

    await repo.update_profile(user, skills="Rust")
    await db_session.commit()

    assert user.skills == "Rust"
    assert user.desired_role == "Go Developer"
