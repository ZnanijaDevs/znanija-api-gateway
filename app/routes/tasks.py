from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.models import BRAINLY_ID, EntryInTaskLog, LegacyQuestion
from app.brainly_api import legacy_api
from app.brainly_api.exceptions import QuestionDoesNotExistException
from app.util import transform_task_log_entries, transform_legacy_task


router = APIRouter(prefix="/tasks")


@router.get("/{id}", response_model=LegacyQuestion | None)
@cache(expire=3)
async def get_task(id: BRAINLY_ID):
    try:
        question = await legacy_api.get_question(id)

        return transform_legacy_task(question.data, question.users_data)
    except QuestionDoesNotExistException:
        return None


@router.get("/{id}/log", response_model=list[EntryInTaskLog])
@cache(expire=1)
async def get_task_log(id: BRAINLY_ID):
    try:
        question_log = await legacy_api.get_question_log(id)

        log_entries = question_log.data
        users_data = question_log.users_data

        return transform_task_log_entries(log_entries, users_data)
    except QuestionDoesNotExistException:
        return []
