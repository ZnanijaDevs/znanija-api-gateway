from pydantic import BaseModel, conint, conlist, constr


BRAINLY_ID = conint(gt=0, lt=1_000_000_000)


class CheckDeletedTasksPayload(BaseModel):
    ids: conlist(item_type=BRAINLY_ID, max_items=100)


class GetBrainlyUsersPayload(BaseModel):
    ids: conlist(item_type=BRAINLY_ID, max_items=1500)


class SendMessageToUserPayload(BaseModel):
    user_id: BRAINLY_ID
    text: constr(max_length=500, min_length=1)
