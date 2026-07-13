from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LikeBase(BaseModel):
    post_id: int
    user_id: int


class LikeCreate(LikeBase):
    pass


class LikeUpdate(BaseModel):
    post_id: int | None = None
    user_id: int | None = None


class LikeRead(LikeBase):
    id: int
    timestamps: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


LikeResponse = LikeRead
UserReponse = LikeRead
