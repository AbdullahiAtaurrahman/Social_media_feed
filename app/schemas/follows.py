from pydantic import BaseModel, ConfigDict


class FollowBase(BaseModel):
    follower_id: int
    following_id: int


class FollowCreate(FollowBase):
    pass


class FollowUpdate(BaseModel):
    follower_id: int | None = None
    following_id: int | None = None


class FollowRead(FollowBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


FollowResponse = FollowRead
FollowReponse = FollowRead
