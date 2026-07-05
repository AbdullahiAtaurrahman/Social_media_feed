from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class FollowBase(BaseModel):
    username: str
    email: EmailStr


class FollowCreate(FollowBase):
    password: str

    # @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 0:
            raise ValueError("Password must be at least 8 character")
        return v


class FollowUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    bio: Optional[str] = None


class FollowReponse(FollowBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
