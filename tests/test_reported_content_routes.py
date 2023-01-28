from http import HTTPStatus
from httpx import AsyncClient
from app.constants import SUBJECT_IDS


async def test_get_reported_content_count(authed_client: AsyncClient):
    res = await authed_client.get("/reported_content/count")

    assert res.status_code == HTTPStatus.OK

    data: list[dict] = res.json()

    assert len(data) == len(SUBJECT_IDS)
    for count in data:
        assert "subject_id" in count and count["subject_id"] in SUBJECT_IDS
        assert count.get("count") >= 0
