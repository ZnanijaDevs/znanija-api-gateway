import asyncio
import httpx

from app.getenv import env
from app.constants import SUBJECT_IDS
from app.models import ReportedContentsCountBySubject


session = httpx.AsyncClient(
    base_url='https://srv-content-classification.z-dn.net/ru/moderation_items/count',
    headers={
        'x-b-token-long': env('BRAINLY_AUTH_TOKEN')
    },
    verify=False,
    timeout=12
)

async def _call(subject_id: int):
    response = await session.get(f"?classified_by=abuse_report&subject_id={subject_id}")

    assert response.status_code == 200, f"fetching reported content count failed: {response.content.decode('utf-8')}"

    data = response.json()

    assert 'count' in data, f"no count in the response: {data}"

    return ReportedContentsCountBySubject(subject_id=subject_id, count=data['count'])


async def get_reported_content_count() -> list[ReportedContentsCountBySubject]:
    """
    Get the number of reported content for each subject.
    This function will definitely be removed in the future, since the count of reported content
    will be available in the GraphQL API.
    """
    results = await asyncio.gather(*[
        asyncio.ensure_future(_call(subject_id)) for subject_id in SUBJECT_IDS
    ])

    return results
