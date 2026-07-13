from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    image_url: Mapped[str] = mapped_column(String(200))
    visibility: Mapped[bool] = mapped_column(default=True)
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
