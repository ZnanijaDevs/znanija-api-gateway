from fastapi import APIRouter

from app.models import GetBrainlyUsersPayload, GetBrainlyUsersWithExtraDataPayload, \
    SendMessageToUserPayload
from app.brainly_api import legacy_api, graphql_api


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

USER_WITH_EXTRA_DATA_FRAGMENT = """
fragment UserWithExtraData on User {
  nick
  avatar {url}
  gender
  points
  statistics {banCount warningCount}
  thanks {count}
  answerCountBySubject {
    count
    markedAsBest
    subject {id name}
  }
  answers {
    count
  }
  created
  rank {name id}
  specialRanks {name id}
  grade {id name}
}
"""

@router.post('/extra_data')
async def get_users_with_extra_data(payload: GetBrainlyUsersWithExtraDataPayload):
    fetched_users = await graphql_api.mapped_query_with_ids(
        payload.ids,
        'user',
        '...UserWithExtraData',
        transform_entry=lambda user: user,#{
        #    'nick': user['nick'],
        #    'avatar': '' if user['avatar'] is None else user['avatar']['url'],
        #    'thanks_count': user['thanks']['count'],
        #    'gender': user['gender'],
        #    'points': user['points'],
        #},
        extra_query=USER_WITH_EXTRA_DATA_FRAGMENT
    )

    return fetched_users


@router.post('/send_message')
async def send_message_to_user(payload: SendMessageToUserPayload):
    message_response = await legacy_api.send_message(payload.user_id, payload.text)

    return message_response['data']
