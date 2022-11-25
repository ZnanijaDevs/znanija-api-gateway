from enum import Enum
from pydantic import BaseModel, conint, conlist, constr


BRAINLY_ID = conint(gt=0, lt=1_000_000_000)


class CheckDeletedTasksPayload(BaseModel):
    ids: conlist(item_type=BRAINLY_ID, max_items=100)


class GetBrainlyUsersPayload(BaseModel):
    ids: conlist(item_type=BRAINLY_ID, max_items=1500)


class SendMessageToUserPayload(BaseModel):
    user_id: BRAINLY_ID
    text: constr(max_length=500, min_length=1)


class BanType(Enum):
    ONE_DAY = 5
    THREE_DAYS = 7
    PERMANENT = 8


class BanUserPayload(BaseModel):
    ban_type: BanType


class ModerationRankingType(Enum):
    MODERATOR_DAILY = 'daily'
    MODERATOR_WEEKLY = 'weekly'
    MODERATOR_MONTHLY = 'monthly'
    MODERATOR_QUARTERLY = 'quarterly'
