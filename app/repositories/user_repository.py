# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from schemas.users import UserCreate, UserUpdate
from app.core.security import hash_password


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    hashed_pw = hash_password(data.password)  # use passlib/bcrypt
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
    )
    db.add(user)  # Stage INSERT
    await db.commit()  # Write to DB
    await db.refresh(user)  # Reload — populates id, created_at, etc.
    return user


# 2


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)  # Fastest — uses primary key


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return await db.execute(stmt).scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return await db.execute(stmt).scalars().all()


# With filtering
async def get_active_users(db: AsyncSession) -> list[User]:
    stmt = select(User).where(User.is_active == True)
    return await db.execute(stmt).scalars().all()


# 3


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> User | None:
    user = await db.get(User, user_id)
    if not user:
        return None

    # model_dump(exclude_unset=True) only returns fields actually sent
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


# 4


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    user = await db.get(User, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
