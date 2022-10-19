from fastapi import APIRouter

from app.models import GetBrainlyUsersPayload, SendMessageToUserPayload
from app.brainly_api import legacy_api
from app.utils.transformers import transform_legacy_user_with_basic_data


router = APIRouter(prefix='/brainly/users')


@router.post('')
async def get_users(payload: GetBrainlyUsersPayload):
    users_data = await legacy_api.get_users(payload.ids)
    users = [transform_legacy_user_with_basic_data(user) for user in users_data['data']]

    return users


@router.post('/send_message')
async def send_message_to_user(payload: SendMessageToUserPayload):
    message_response = await legacy_api.send_message(payload.user_id, payload.text)

    return message_response['data']
