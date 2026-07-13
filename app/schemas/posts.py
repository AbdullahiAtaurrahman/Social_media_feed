from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    image_url: str | None = None
    visibility: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    image_url: str | None = None
    visibility: bool | None = None


class PostRead(PostBase):
    id: int
    user_id: int
    timestamps: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


PostResponse = PostRead
PostReponse = PostRead
PserUpdate = PostUpdate
