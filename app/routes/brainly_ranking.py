from fastapi import APIRouter

from app.brainly_api import graphql_api, to_id, from_id
from app.constants import DISALLOWED_RANKS_FOR_ACTIVE_USERS, MIN_ANSWERS_COUNT_FOR_ACTIVE_USER, \
    SUBJECT_IDS, RANKING_TYPES


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
                '{ user {...UserInUserRanking} } '
            ])

    data = await graphql_api.query("""
    fragment UserInUserRanking on User {
        id
        answers {count}
        specialRanks {name}
        rank {id name}
    }
    query {""" + rankings_query_pieces + '}')

    active_users_ids = set()
    active_users = []

    for places in data.values():
        for place in places:
            user = place.get('user') or {}
            user_id = user.get('id')

            if user_id is None or user_id in active_users_ids:
                continue

            user_rank = None if user['rank'] is None else user['rank']['name']
            answers_count = user['answers']['count']

            if (
                len(user['specialRanks']) > 0 or
                user_rank is None or
                user_rank in DISALLOWED_RANKS_FOR_ACTIVE_USERS or
                answers_count < MIN_ANSWERS_COUNT_FOR_ACTIVE_USER
            ):
                continue

            active_users.append(from_id(user_id))
            active_users_ids.add(user_id)

    return active_users
