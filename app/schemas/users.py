from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str = None
    email: EmailStr


class UserCreate(User):
    role: str
    password: str
