import re
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.brainly_api import get_parsed_page
from app.constants import DEFAULT_USER_AVATAR, EXCLUDE_MODERATORS_FROM_MODS_LIST, \
    SPAMOUTS_AND_MODS_RANKS_REGEX
from app.models import ModeratorInModeratorsList


router = APIRouter(prefix="/moderators")


@router.get("", response_model=list[ModeratorInModeratorsList])
@cache(expire=30, namespace="get-moderators-list")
async def get_moderators_list():
    moderators_page = await get_parsed_page("/moderators/mod_list?limit=500")

    user_data_elements = moderators_page(".usersTable .user-data").items()
    moderators: list[ModeratorInModeratorsList] = []

    for element in user_data_elements:
        user_id = int(element("a").attr("href").split("-").pop())
        user_ranks = element(".user-nick span").map(lambda _, element: element.text.strip())
        avatar_src = element("img").attr("src")

        if len(user_ranks) == 0 or user_id in EXCLUDE_MODERATORS_FROM_MODS_LIST:
            continue

        user_ranks_as_str = "\n".join(user_ranks).lower()
        is_spamout_or_moderator = re.search(SPAMOUTS_AND_MODS_RANKS_REGEX, user_ranks_as_str) is not None

        if is_spamout_or_moderator:
            moderators.append(ModeratorInModeratorsList(
                id=user_id,
                nick=element(".nick").text(),
                ranks=element(".user-nick span").map(lambda _, element: element.text.strip()),
                avatar=DEFAULT_USER_AVATAR if "img" in avatar_src else avatar_src
            ))

    return moderators
