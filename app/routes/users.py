from fastapi import APIRouter, Query
from pydantic import conlist

from app.models import SendMessageToUserPayload, BanUserPayload, BRAINLY_ID, LegacyUserWithBasicData, \
    BanUserResponse, CancelBanResponse, SendMessageToUserResponse
from app.brainly_api import legacy_api, get_form_data_from_user_page, send_form
from app.util import transform_legacy_user_with_basic_data


router = APIRouter(prefix="/users")


@router.get("", response_model=list[LegacyUserWithBasicData])
async def get_users(
    user_ids: conlist(item_type=BRAINLY_ID) = Query(alias="ids[]")
):
    users_data = await legacy_api.get_users(user_ids)
    users = [transform_legacy_user_with_basic_data(user) for user in users_data.data]

    return users


@router.post("/send_message", response_model=SendMessageToUserResponse)
async def send_message_to_user(payload: SendMessageToUserPayload):
    message_response = await legacy_api.send_message(payload.user_id, payload.text)

    return message_response.data


@router.post("/{user_id}/ban", response_model=BanUserResponse)
async def ban_user(user_id: BRAINLY_ID, payload: BanUserPayload):
    ban_payload = await get_form_data_from_user_page(user_id, "#UserBanAddForm")
    ban_payload["data[UserBan][type]"] = str(payload.ban_type.value)

    await send_form(f"/bans/ban/{user_id}", ban_payload)

    return BanUserResponse(ban_type=payload.ban_type)


@router.post("/{user_id}/cancel_ban", response_model=CancelBanResponse)
async def cancel_ban(user_id: BRAINLY_ID):
    await send_form(f"/bans/cancel/{user_id}")

    return CancelBanResponse()
