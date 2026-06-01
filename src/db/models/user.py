from sqlalchemy import BigInteger, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255))

    skills: Mapped[str | None] = mapped_column(Text)
    experience: Mapped[str | None] = mapped_column(Text)
    desired_role: Mapped[str | None] = mapped_column(String(255))
    desired_salary: Mapped[int | None] = mapped_column()
    location: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    saved_searches: Mapped[list["SavedSearch"]] = relationship(back_populates="user")  # noqa: F821
    saved_vacancies: Mapped[list["SavedVacancy"]] = relationship(back_populates="user")  # noqa: F821
