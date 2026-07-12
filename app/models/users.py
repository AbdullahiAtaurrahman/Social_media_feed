from typing import List, Optional, TYPE_CHECKING
from core.db_async import Base
from sqlalchemy.orm import file, Mapped, mapped_column
from sqlalchemy import func, String, Text
from datetime import datetime

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.comments import Comment
    from app.models.posts import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    role: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    bio: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(String(200), index=True, unique=True)
    avatar_url: file
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=True)

    posts: List["Post"] = []
    comments: List["Comment"] = []
