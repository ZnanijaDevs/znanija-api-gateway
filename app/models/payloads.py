from pydantic import BaseModel, conlist, constr
from .entities import BRAINLY_ID, BanType


class CheckDeletedTasksPayload(BaseModel):
    ids: conlist(item_type=BRAINLY_ID, max_items=100)


class SendMessageToUserPayload(BaseModel):
    user_id: BRAINLY_ID
    text: constr(max_length=500, min_length=1)


class BanUserPayload(BaseModel):
    ban_type: BanType
