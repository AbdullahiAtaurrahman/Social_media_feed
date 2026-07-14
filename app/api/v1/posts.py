from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db_async
from app.models.posts import Post
from app.schemas.posts import PostCreate, PostRead, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])


async def get_post_or_404(db: AsyncSession, post_id: int) -> Post:
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


@router.get("/", response_model=list[PostRead])
async def list_posts(
    db: AsyncSession = Depends(get_db_async),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
) -> list[Post]:
    result = await db.execute(select(Post).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db_async)) -> Post:
    return await get_post_or_404(db, post_id)


@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreate,
    user_id: int = Query(..., ge=1),
    db: AsyncSession = Depends(get_db_async),
) -> Post:
    post = Post(
        title=payload.title,
        content=payload.content,
        image_url=payload.image_url,
        visibility=payload.visibility,
        user_id=user_id,
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    db: AsyncSession = Depends(get_db_async),
) -> Post:
    post = await get_post_or_404(db, post_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    await db.commit()
    await db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db_async)) -> None:
    post = await get_post_or_404(db, post_id)
    await db.delete(post)
    await db.commit()
