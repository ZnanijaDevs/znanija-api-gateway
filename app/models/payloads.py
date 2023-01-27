from pydantic import BaseModel, constr
from .entities import BRAINLY_ID, BanType


class SendMessageToUserPayload(BaseModel):
    user_id: BRAINLY_ID
    text: constr(max_length=500, min_length=1)


class BanUserPayload(BaseModel):
    ban_type: BanType
