from typing import Generator
from functools import cache
from copy import deepcopy
import pytest
from asyncio import get_event_loop
from httpx import AsyncClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from app.main import app
from app.getenv import env


@pytest.fixture(scope="module")
async def async_client() -> Generator:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(scope="module")
async def authed_client(async_client: AsyncClient):
    async with AsyncClient(
        app=app,
        auth=(env("AUTH_USER"), env("AUTH_PASSWORD")),
        base_url="http://authed_testserver"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
def cache_setup():
    FastAPICache.init(InMemoryBackend())


@pytest.fixture(scope="module")
def event_loop():
    loop = get_event_loop()

    yield loop
