from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base, TimestampMixin


class SavedSearch(Base, TimestampMixin):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    query: Mapped[str] = mapped_column(String(512))
    filters_json: Mapped[str | None] = mapped_column(Text)
    name: Mapped[str | None] = mapped_column(String(255))

    user: Mapped["User"] = relationship(back_populates="saved_searches")  # noqa: F821
