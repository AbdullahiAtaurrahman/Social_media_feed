from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class LikeBase(BaseModel):
    username: str
    email: EmailStr


class LikeCreate(LikeBase):
    password: str

    # @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 0:
            raise ValueError("Password must be at least 8 character")
        return v


class LikeUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class UserReponse(LikeBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
