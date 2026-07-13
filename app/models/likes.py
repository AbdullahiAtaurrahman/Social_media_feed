from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
