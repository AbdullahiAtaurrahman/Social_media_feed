from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: str | None = None


class CommentRead(CommentBase):
    id: int
    user_id: int
    post_id: int
    timestamps: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


CommentResponse = CommentRead
CommentReponse = CommentRead
