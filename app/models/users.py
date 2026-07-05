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

    id: int
    username: str
    email: str
    password: str
    bio: str
    avatar_url: file
    role: str
    timestamps: Mapped[datetime | None] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = []
    comments: List["Comment"] = []
