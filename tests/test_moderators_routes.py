from http import HTTPStatus
from httpx import AsyncClient


async def test_get_moderators_list(authed_client: AsyncClient):
    res = await authed_client.get("/moderators")

    assert res.status_code == HTTPStatus.OK

    moderators: list[dict] = res.json()

    assert len(moderators) > 1
    for moderator in moderators:
        assert moderator["id"] > 0
        assert isinstance(moderator.get("avatar"), str)
        assert isinstance(moderator.get("nick"), str)
        assert "ranks" in moderator and len(moderator["ranks"]) > 0
