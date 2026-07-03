from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Like(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(autoincrement="true")
    user_id: Mapped[int] = mapped_column(ForeignKey(users.id))
    title: Mapped[str] = mapped_column(String(50))
    image_url: Mapped[str] = mapped_column(String(200), nullablle="True")
    visibility: Mapped[str] = mapped_column(bool=True)
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
