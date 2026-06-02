from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create_user(
        self,
        telegram_id: int,
        *,
        username: str | None = None,
        full_name: str | None = None,
    ) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.username = username
            user.full_name = full_name
            return user
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        self.session.add(user)
        await self.session.flush()
        return user

    async def create_profile(
        self,
        db_user: dict,
        *,
        skills: str | None = None,
        experience: str | None = None,
        desired_role: str | None = None,
        desired_salary: int | None = None,
        location: str | None = None,
    ) -> User:
        user = User(
            **db_user,
            skills=skills,
            experience=experience,
            desired_role=desired_role,
            desired_salary=desired_salary,
            location=location,
            )
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_profile(
        self,
        user: User,
        *,
        skills: str | None = None,
        experience: str | None = None,
        desired_role: str | None = None,
        desired_salary: int | None = None,
        location: str | None = None,
    ) -> User:
        if skills is not None:
            user.skills = skills
        if experience is not None:
            user.experience = experience
        if desired_role is not None:
            user.desired_role = desired_role
        if desired_salary is not None:
            user.desired_salary = desired_salary
        if location is not None:
            user.location = location
        await self.session.commit()
        return user
