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
    TUTORIAL = 1
    FIFTEEN_MINUTES = 2
    ONE_HOUR = 3
    TWELVE_HOURS = 4
    TWENTY_FOUR_HOURS = 5
    FOURTY_EIGHT_HOURS = 6


class BanUserPayload(BaseModel):
    ban_type: BanType
