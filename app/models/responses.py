from pydantic import BaseModel
from .entities import BanType, FeedNode


class BanUserResponse(BaseModel):
    ban_type: BanType
    banned: bool = True


class CancelBanResponse(BaseModel):
    cancelled: bool = True


class SendMessageToUserResponse(BaseModel):
    content: str
    conversation_id: int
    created: str
    id: int
    is_harmful: bool
    user_id: int


class GetFeedResponse(BaseModel):
    nodes: list[FeedNode]
    end_cursor: str
