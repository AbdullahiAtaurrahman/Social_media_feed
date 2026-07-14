from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Like
from schemas.likes import LikeCreate


class LikeRepository:
    @staticmethod
    async def create_like(db: AsyncSession, post_id: int, user_id: int) -> Like:
        like = Like(post_id=post_id, user_id=user_id)
        db.add(like)
        await db.commit()
        await db.refresh(like)
        return like

    @staticmethod
    async def get_like(db: AsyncSession, post_id: int, user_id: int) -> Like | None:
        stmt = select(Like).where(Like.post_id == post_id, Like.user_id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def delete_like(db: AsyncSession, like: Like) -> None:
        db.delete(like)
        await db.commit()
