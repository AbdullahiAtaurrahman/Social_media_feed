from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from app.core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Follow(Base):
    __tablename__ = "follows"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
