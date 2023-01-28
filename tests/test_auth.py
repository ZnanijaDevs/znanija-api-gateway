from http import HTTPStatus
from httpx import AsyncClient


async def test_auth(authed_client: AsyncClient):
    res = await authed_client.get("/")
    assert res.status_code == HTTPStatus.OK


async def test_no_auth(async_client: AsyncClient):
    res = await async_client.get("/")
    assert res.status_code == HTTPStatus.UNAUTHORIZED
