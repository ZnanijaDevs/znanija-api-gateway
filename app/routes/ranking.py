from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.brainly_api import graphql_api, to_id, from_id
from app.models import ModerationRankingType, PlaceInModeratorsRanking, TransformedGraphqlUser
from app.constants import DISALLOWED_RANKS_FOR_ACTIVE_USERS, MIN_ANSWERS_COUNT_FOR_ACTIVE_USER, \
    SUBJECTS_IDS_FOR_ACTIVE_USERS, RANKING_TYPES
from app.brainly_api.graphql_queries import USER_WITH_ANSWERS_COUNT_FRAGMENT, \
    GET_MODERATION_RANKING_QUERY
from app.util import transform_gql_user


router = APIRouter(prefix="/ranking")


@router.get("/moderators/{ranking_type}", response_model=list[PlaceInModeratorsRanking])
@cache(expire=5, namespace="get-moderator-daily-ranking")
async def get_moderator_daily_ranking(ranking_type: ModerationRankingType):
    rankings_data = await graphql_api.query(GET_MODERATION_RANKING_QUERY, {
        "type": ranking_type.name
    })

    rankings: list[PlaceInModeratorsRanking] = []
    for place in rankings_data["userRankings"]:
        moderator = place["user"]
        if moderator is None or len(moderator["specialRanks"]) == 0:
            continue

        rankings.append(PlaceInModeratorsRanking(
            points=place["points"],
            user_id=from_id(place["user"]["id"]),
            user_nick=moderator["nick"],
            user_ranks=[rank["name"] for rank in moderator["specialRanks"]]
        ))

    return rankings


@router.get("/active_users", response_model=list[TransformedGraphqlUser])
@cache(expire=60, namespace="get-active-users-from-rankings")
async def get_active_users_from_rankings():
    rankings_query_pieces = ""
    for ranking_type in RANKING_TYPES:
        for subject_id in SUBJECTS_IDS_FOR_ACTIVE_USERS:
            rankings_query_pieces += "".join([
                f"s{subject_id}s{ranking_type}: ",
                f"userRankingBySubjectId(rankingType: {ranking_type},",
                f"subjectId: \"{to_id(subject_id, 'subject')}\") ",
                "{ user {id answers {count} rank {name} specialRanks {name}} } "
            ])

    data = await graphql_api.query("query {" + rankings_query_pieces + "}")

    active_users_ids = set()

    for places in data.values():
        for place in places:
            user = place.get("user")

            if user is None:
                continue

            user_id = from_id(user["id"])

            if (
                user_id is None or
                user_id in active_users_ids or
                len(user["specialRanks"]) > 0 or
                user["rank"] is None or
                user["rank"]["name"] in DISALLOWED_RANKS_FOR_ACTIVE_USERS or
                user["answers"]["count"] < MIN_ANSWERS_COUNT_FOR_ACTIVE_USER
            ):
                continue

            active_users_ids.add(user_id)

    users_data: list[TransformedGraphqlUser] = await graphql_api.mapped_query_with_ids(
        list(active_users_ids),
        "user",
        "...UserWithAnswersCount",
        transform_entry=transform_gql_user,
        extra_query=USER_WITH_ANSWERS_COUNT_FRAGMENT
    )

    return users_data
