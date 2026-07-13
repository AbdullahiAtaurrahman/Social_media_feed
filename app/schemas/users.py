from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str | None = None
    bio: str | None = None


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    bio: str | None = None
    role: str | None = None


class UserRead(UserBase):
    id: int
    is_active: bool = True
    is_superuser: bool = False
    timestamps: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


UserResponse = UserRead
UserReponse = UserRead
