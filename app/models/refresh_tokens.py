from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime


from core.db_async import Base

if TYPE_CHECKING:
    from app.models.users import User


class Follow(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(autoincrement="true")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[int] = mapped_column(ForeignKey("users.id"))
    revoked_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    expires_at: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


Owner: Mapped["User"] = relationship("User", back_populates="posts", lazy="joined")
