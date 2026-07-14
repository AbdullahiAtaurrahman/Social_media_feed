from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Comment
from schemas.comments import CommentCreate


class CommentRepository:
    @staticmethod
    async def create_comment(
        db: AsyncSession, post_id: int, user_id: int, content: str
    ) -> Comment:
        comment = Comment(post_id=post_id, user_id=user_id, content=content)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_comments_by_post(db: AsyncSession, post_id: int) -> list[Comment]:
        stmt = select(Comment).where(Comment.post_id == post_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def delete_comment(db: AsyncSession, comment: Comment) -> None:
        await db.delete(comment)
        await db.commit()
