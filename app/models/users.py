from typing import List, Optional, TYPE_CHECKING
from core.db_async import Base

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
    is_active: bool = True
    is_superuser: bool = False

    posts: List["Post"] = []
    comments: List["Comment"] = []
