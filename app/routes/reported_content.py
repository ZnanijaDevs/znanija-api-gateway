from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.brainly_api import get_reported_content_count as fetch_reported_content
from app.models import ReportedContentsCountBySubject


router = APIRouter(prefix="/reported_content")


@router.get("/count", response_model=list[ReportedContentsCountBySubject])
@cache(expire=5)
async def get_reported_content_count():
    return await fetch_reported_content()
