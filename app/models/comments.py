from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(autoincrement="true")
    post_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(String(50))
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
