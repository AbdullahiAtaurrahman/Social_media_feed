from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository
from app.models.users import User


from sqlalchemy.orm import SessionLocal
from sqlalchemy.orm import AsyncSessionLocal


# Synchronous
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Async
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exc
    except JWTError:
        raise credentials_exc
    user = UserRepository.get_by_username(db, username)
    if user is None:
        raise credentials_exc
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(*roles: str):
    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {roles}. You have: {current_user.role}",
            )
        return current_user

    return role_checker


require_admin = require_role("admin")
require_staff = require_role("admin", "moderator")
