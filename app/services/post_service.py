# from fastapi import HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from app.models.posts import Post


# class PostService:
#     @staticmethod
#     async def get_post_by_id(db: AsyncSession, post_id: int):
#         stmt = select(Post).where(Post.id == post_id)
#         result = await db.execute(stmt)
#         post = result.scalars().first()
#         if not post:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail=f"Post with id {post_id} not found",
#             )
#         return post

#     @staticmethod
#     async def get_all_posts(db: AsyncSession, skip: int = 0, limit: int = 20):
#         stmt = select(Post).offset(skip).limit(limit)
#         result = await db.execute(stmt)
#         return result.scalars().all()

#     @staticmethod
#     async def create_post(db: AsyncSession, title: str, content: str, user_id: int):
#         new_post = Post(title=title, content=content, user_id=user_id)
#         db.add(new_post)
#         await db.commit()
#         await db.refresh(new_post)
#         return new_post

#     @staticmethod
#     async def update_post(
#         db: AsyncSession,
#         post_id: int,
#         title: str | None = None,
#         content: str | None = None,
#     ):
#         post = await PostService.get_post_by_id(db, post_id)
#         if title is not None:
#             post.title = title
#         if content is not None:
#             post.content = content
#         await db.commit()
#         await db.refresh(post)
#         return post

#     @staticmethod
#     async def delete_post(db: AsyncSession, post_id: int):
#         post = await PostService.get_post_by_id(db, post_id)
#         await db.delete(post)
#         await db.commit()
#         return {"detail": f"Post with id {post_id} deleted successfully"}

#     @staticmethod
#     async def get_posts_by_user(
#         db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20
#     ):
#         stmt = select(Post).where(Post.user_id == user_id).offset(skip).limit(limit)
#         result = await db.execute(stmt)
#         return result.scalars().all()

#     @staticmethod
#     async def get_posts_by_user_paginated(
#         db: AsyncSession, user_id: int, skip: int = 0, limit: int = 20
#     ):
#         stmt = select(Post).where(Post.user_id == user_id)
#         count_result = await db.execute(
#             select(func.count()).select_from(stmt.subquery())
#         )
#         total = count_result.scalar()
#         stmt = stmt.offset(skip).limit(limit)
#         result = await db.execute(stmt)
#         posts = result.scalars().all()
#         return posts, total

#     @staticmethod
#     async def get_all_posts_paginated(db: AsyncSession, skip: int = 0, limit: int = 20):
#         stmt = select(Post)
#         count_result = await db.execute(
#             select(func.count()).select_from(stmt.subquery())
#         )
#         total = count_result.scalar()
#         stmt = stmt.offset(skip).limit(limit)
#         result = await db.execute(stmt)
#         posts = result.scalars().all()
#         return posts, total

#     @staticmethod
#     async def get_posts_by_user_paginated_with_search(
#         db: AsyncSession,
#         user_id: int,
#         skip: int = 0,
#         limit: int = 20,
#         search: str | None = None,
#     ):
#         stmt = select(Post).where(Post.user_id == user_id)
#         if search:
#             stmt = stmt.where(Post.title.ilike(f"%{search}%"))
#         count_result = await db.execute(
#             select(func.count()).select_from(stmt.subquery())
#         )
#         total = count_result.scalar()
#         stmt = stmt.offset(skip).limit(limit)
#         result = await db.execute(stmt)
#         posts = result.scalars().all()
#         return posts, total
