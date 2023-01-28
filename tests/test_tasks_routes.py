import pytest
from http import HTTPStatus
from httpx import AsyncClient
from .util import expect_result


@pytest.mark.parametrize("task_id", [8])
async def test_get_task_by_id(authed_client: AsyncClient, task_id: int):
    res = await authed_client.get(f"/tasks/{task_id}")

    expect_result(res, f"responses/get_task_by_id_{task_id}.json")


@pytest.mark.parametrize("invalid_task_id", [-3, 1e12])
async def test_get_task_by_invalid_id(authed_client: AsyncClient, invalid_task_id: int):
    res = await authed_client.get(f"/tasks/{invalid_task_id}")
    assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("deleted_task_id", [565, 9999999999])
async def test_get_deleted_task_by_id(authed_client: AsyncClient, deleted_task_id: int):
    res = await authed_client.get(f"/tasks/{deleted_task_id}")

    assert res.status_code == HTTPStatus.OK
    assert res.json() is None


@pytest.mark.parametrize("task_id", [11613660])
async def test_get_task_log(authed_client: AsyncClient, task_id: int):
    res = await authed_client.get(f"/tasks/{task_id}/log")

    expect_result(res, f"responses/get_task_log_by_id_{task_id}.json")


@pytest.mark.parametrize("task_id", [1, 6])
async def test_get_deleted_task_log(authed_client: AsyncClient, task_id: int):
    res = await authed_client.get(f"/tasks/{task_id}/log")

    assert res.status_code == HTTPStatus.OK
    assert res.json() == []
