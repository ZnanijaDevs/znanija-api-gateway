import pytest
from http import HTTPStatus
from httpx import AsyncClient
from .util import expect_result


USER_ID_FOR_TESTING = 29489586


@pytest.mark.parametrize("user_ids", [[1, 2, 27630562]])
async def test_get_users(authed_client: AsyncClient, user_ids: list[int]):
    request_path = "/users"
    for user_id in user_ids:
        request_path += f"{'?' if request_path.endswith('users') else '&'}ids[]={user_id}"

    res = await authed_client.get(request_path)
    expect_result(res, "responses/get_users.json")


async def test_get_users_with_invalid_ids(authed_client: AsyncClient):
    res = await authed_client.get("/users?ids[]=2&ids[]=-340")
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("user_id", [USER_ID_FOR_TESTING])
async def test_send_message(authed_client: AsyncClient, user_id: int):
    res = await authed_client.post("/users/send_message", json={
        "user_id": user_id,
        "text": "Test message"
    })

    assert res.status_code == HTTPStatus.OK


@pytest.mark.parametrize("user_id", [USER_ID_FOR_TESTING])
async def test_ban_user(authed_client: AsyncClient, user_id: int):
    BAN_TYPE = 5

    res = await authed_client.post(f"/users/{user_id}/ban", json={
        "ban_type": BAN_TYPE
    })
    data: dict = res.json()

    assert data.get("banned") is True
    assert data.get("ban_type") == BAN_TYPE


@pytest.mark.parametrize("user_id", [USER_ID_FOR_TESTING])
async def test_cancel_ban(authed_client: AsyncClient, user_id: int):
    res = await authed_client.post(f"/users/{user_id}/cancel_ban")
    data: dict = res.json()

    assert data.get("cancelled") is True
