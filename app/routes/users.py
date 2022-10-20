from fastapi import APIRouter

from app.models import GetBrainlyUsersPayload, SendMessageToUserPayload, BanUserPayload, \
    BRAINLY_ID
from app.brainly_api import legacy_api, get_form_data_from_user_page, send_form
from app.utils.transformers import transform_legacy_user_with_basic_data


router = APIRouter(prefix='/brainly/users')


@router.post('')
async def get_users(payload: GetBrainlyUsersPayload):
    users_data = await legacy_api.get_users(payload.ids)
    users = [transform_legacy_user_with_basic_data(user) for user in users_data.data]

    return users


@router.post('/send_message')
async def send_message_to_user(payload: SendMessageToUserPayload):
    message_response = await legacy_api.send_message(payload.user_id, payload.text)

    return message_response.data


@router.post('/{user_id}/ban')
async def ban_user(user_id: BRAINLY_ID, payload: BanUserPayload):
    ban_payload = await get_form_data_from_user_page(user_id, '#UserBanAddForm')
    ban_payload['data[UserBan][type]'] = str(payload.ban_type.value)

    await send_form(f"/bans/ban/{user_id}", ban_payload)

    return {
        'banned': True,
        'user_id': user_id,
        'ban_type': payload.ban_type
    }


@router.post('/{user_id}/cancel_ban')
async def cancel_ban(user_id: BRAINLY_ID):
    await send_form(f"/bans/cancel/{user_id}")

    return {'ban_cancelled': True}
