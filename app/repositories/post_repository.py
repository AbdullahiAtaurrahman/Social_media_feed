from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from models import Post
from schemas.posts import PostCreate, PostUpdate
from app.core.security import hash_password


class PostRepository:
    @staticmethod
    async def get_by_id(db: AsyncSession, post_id: int) -> Post | None:
        result = await db.execute(
            select(Post).where(Post.id == post_id).options(selectinload(Post.owner))
        )
        return result.scalars().first()

    @staticmethod
    async def get_all_paginated(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> tuple[list[Post], int]:
        # cache_key = f"posts:list:{skip}:{limit}:{search or ''}"
        # cached = await cache_get(cache_key)
        # if cached:
        #     # Return cached payload — items are dicts not ORM objects here
        #     return cached["items"], cached["total"]

        stmt = select(Post).options(selectinload(Post.owner))

        if search:
            stmt = stmt.where(Post.title.ilike(f"%{search}%"))

        # Count total (for pagination metadata)
        count_result = await db.execute(
            select(func.count()).select_from(stmt.subquery())
        )
        total = count_result.scalar()

        stmt = stmt.order_by(Post.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        posts = result.scalars().all()

        # Serialise to dict for caching (ORM objects are not JSON-serialisable)
        serialised = [
            {
                "id": p.id,
                "title": p.title,
                "content": p.content,
                "user_id": p.user_id,
                "created_at": p.created_at.isoformat(),
            }
            for p in posts
        ]
        # await cache_set(cache_key, {"items": serialised, "total": total}, ttl=60)

        return posts, total

    @staticmethod
    async def get_by_user(db: AsyncSession, user_id: int) -> list[Post]:
        result = await db.execute(
            select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, data: PostCreate, user_id: int) -> Post:
        post = Post(title=data.title, content=data.content, user_id=user_id)
        db.add(post)
        await db.flush()
        await db.refresh(post)
        # Invalidate list cache so new post appears immediately
        # await cache_delete_pattern("posts:list:*")
        return post

    @staticmethod
    async def update(db: AsyncSession, post: Post, data: PostUpdate) -> Post:
        fields = data.model_dump(exclude_unset=True)
        for key, value in fields.items():
            setattr(post, key, value)
        await db.flush()
        await db.refresh(post)
        # await cache_delete_pattern("posts:list:*")
        return post

    @staticmethod
    async def delete(db: AsyncSession, post: Post) -> None:
        await db.delete(post)
        await db.flush()
        # await cache_delete_pattern("posts:list:*")
