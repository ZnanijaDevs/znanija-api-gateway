from fastapi import APIRouter

from app.brainly_api import graphql_api, to_id, from_id
from app.constants import DISALLOWED_RANKS_FOR_ACTIVE_USERS, MIN_ANSWERS_COUNT_FOR_ACTIVE_USER, \
    SUBJECT_IDS, RANKING_TYPES
from app.brainly_api.graphql_queries import USER_WITH_ANSWERS_COUNT_FRAGMENT
from app.utils.transformers import transform_gql_user


router = APIRouter(prefix='/brainly/ranking')


@router.get('/active_users')
async def get_active_users_from_rankings():
    rankings_query_pieces = ''
    for ranking_type in RANKING_TYPES:
        for subject_id in SUBJECT_IDS:
            rankings_query_pieces += ''.join([
                f"s{subject_id}s{ranking_type}: ",
                f"userRankingBySubjectId(rankingType: {ranking_type},",
                f"subjectId: \"{to_id(subject_id, 'subject')}\") ",
                '{ user {id answers {count} rank {name} specialRanks {name}} } '
            ])

    data = await graphql_api.query('query {' + rankings_query_pieces + '}')

    active_users_ids = set()

    for places in data.values():
        for place in places:
            user = place.get('user')

            if user is None:
                continue

            user_id = from_id(user['id'])

            if (
                user_id is None or
                user_id in active_users_ids or
                len(user['specialRanks']) > 0 or
                user['rank'] is None or
                user['rank']['name'] in DISALLOWED_RANKS_FOR_ACTIVE_USERS or
                user['answers']['count'] < MIN_ANSWERS_COUNT_FOR_ACTIVE_USER
            ):
                continue

            active_users_ids.add(user_id)

    users_data = await graphql_api.mapped_query_with_ids(
        list(active_users_ids),
        'user',
        '...UserWithAnswersCount',
        transform_entry=transform_gql_user,
        extra_query=USER_WITH_ANSWERS_COUNT_FRAGMENT
    )

    return users_data
