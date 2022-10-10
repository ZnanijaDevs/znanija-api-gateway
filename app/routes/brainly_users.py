from fastapi import APIRouter

from app.models import GetBrainlyUsersPayload, SendMessageToUserPayload
from app.brainly_api import legacy_api


router = APIRouter(prefix='/brainly/users')


@router.post('')
async def get_users(payload: GetBrainlyUsersPayload):
    users_data = await legacy_api.get_users(payload.ids)
    users = []

    for user in users_data['data']:
        user_avatar = user['avatar']['medium'] if user['avatar'] else None

        users.append({
            'nick': user['nick'],
            'id': user['id'],
            'is_deleted': user['is_deleted'],
            'avatar': user_avatar,
        })

    return users


@router.post('/send_message')
async def send_message_to_user(payload: SendMessageToUserPayload):
    message_response = await legacy_api.send_message(payload.user_id, payload.text)

    return message_response['data']
