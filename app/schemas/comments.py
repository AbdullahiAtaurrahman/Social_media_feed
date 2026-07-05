from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    username: str
    email: EmailStr


class CommentCreate(CommentBase):
    password: str

    # @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 0:
            raise ValueError("Password must be at least 8 character")
        return v


class CommentUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class CommentReponse(CommentBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
