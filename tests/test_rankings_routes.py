import pytest
from http import HTTPStatus
from httpx import AsyncClient


@pytest.mark.parametrize("ranking_type", ["daily", "weekly", "monthly", "quarterly"])
async def test_get_moderator_rankings(authed_client: AsyncClient, ranking_type: str):
    res = await authed_client.get(f"/ranking/moderators/{ranking_type}")

    assert res.status_code == HTTPStatus.OK

    rankings = res.json()
    for place in rankings:
        assert place.get("points") > 0
        assert place.get("user_id") > 0
        assert isinstance(place.get("user_nick"), str) and len(place["user_nick"]) > 0
        assert isinstance(place.get("user_ranks"), list)


async def test_get_moderator_rankings_with_invalid_ranking_type(authed_client: AsyncClient):
    res = await authed_client.get("/ranking/moderators/dailyweekly_")

    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_get_active_users_from_rankings(authed_client: AsyncClient):
    res = await authed_client.get("/ranking/active_users")

    assert res.status_code == HTTPStatus.OK

    users: list[dict] = res.json()
    assert len(users) > 0
