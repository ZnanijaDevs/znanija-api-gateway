from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.brainly_api import get_parsed_page
from app.constants import DEFAULT_USER_AVATAR, SPAMOUTS_TEAM_RANKS, MODERATORS_TEAM_RANKS
from app.models import ModerationTeam, ModeratorInModeratorsList


router = APIRouter(prefix='/brainly/moderators')


@router.get('', response_model=list[ModeratorInModeratorsList])
@cache(expire=15, namespace='get-moderators-list')
async def get_moderators_list(team: ModerationTeam | None = ModerationTeam.ALL):
    moderators_page = await get_parsed_page('/moderators/mod_list?limit=500')

    user_data_elements = moderators_page('.usersTable .user-data').items()
    moderators: list[ModeratorInModeratorsList] = []

    for element in user_data_elements:
        user_id = int(element('a').attr('href').split('-').pop())
        user_ranks = element('.user-nick span').map(lambda _, element: element.text.strip())
        avatar_src = element('img').attr('src')

        if (
            len(user_ranks) == 0 or
            (team == ModerationTeam.SPAMOUTS and user_ranks[0] not in SPAMOUTS_TEAM_RANKS) or
            (team == ModerationTeam.MODERATORS and user_ranks[0] not in MODERATORS_TEAM_RANKS)
        ):
            continue

        moderators.append(ModeratorInModeratorsList(
            id=user_id,
            nick=element('.nick').text(),
            ranks=element('.user-nick span').map(lambda _, element: element.text.strip()),
            avatar=DEFAULT_USER_AVATAR if 'img' in avatar_src else avatar_src
        ))

    return moderators
