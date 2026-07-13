from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    bio: Mapped[str | None] = mapped_column(Text)
    profile_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # uselist=False enforces the one-to-one constraint at the ORM level
    user: Mapped["User"] = relationship("User", back_populates="profile", uselist=False)
