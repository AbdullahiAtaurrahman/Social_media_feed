from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Follow
from schemas.follows import FollowCreate


class FollowRepository:
    @staticmethod
    async def create_follow(db: AsyncSession, follow_data: FollowCreate) -> Follow:
        follow = Follow(**follow_data.dict())
        db.add(follow)
        await db.commit()
        await db.refresh(follow)
        return follow

    @staticmethod
    async def get_follow(
        db: AsyncSession, follower_id: int, followed_id: int
    ) -> Follow | None:
        stmt = select(Follow).where(
            Follow.follower_id == follower_id, Follow.followed_id == followed_id
        )
        result = await db.execute(stmt)
        return result.scalars().first()

    @staticmethod
    async def delete_follow(db: AsyncSession, follow: Follow) -> None:
        await db.delete(follow)
        await db.commit()
