from fastapi import APIRouter

from app.models import BRAINLY_ID, CheckDeletedTasksPayload
from app.brainly_api import legacy_api, graphql_api
from app.brainly_api.exceptions import QuestionDoesNotExistException
from app.utils.transformers import transform_task_node, transform_log_entry


router = APIRouter(prefix='/brainly/task')


@router.get('/{id}')
async def get_task(id: BRAINLY_ID):
    try:
        question = await legacy_api.get_question(id)

        task = question['data']['task']
        responses = question['data']['responses']
        users_data = question['users_data']

        return {
            'task': transform_task_node(task, users_data),
            'responses': [transform_task_node(response, users_data) for response in responses],
            'responses_count': len(responses)
        }
    except QuestionDoesNotExistException:
        return None


@router.get('/log/{id}')
async def get_task_log(id: BRAINLY_ID):
    try:
        question_log = await legacy_api.get_question_log(id)

        log_entries = question_log['data']
        users_data = question_log['users_data']

        return [transform_log_entry(entry, users_data) for entry in log_entries]
    except QuestionDoesNotExistException:
        return []


@router.post('/deleted_tasks')
async def check_deleted_tasks(payload: CheckDeletedTasksPayload):
    fetched_questions = await graphql_api.mapped_query_with_ids(
        payload.ids,
        'question',
        'id',
        transform_entry=lambda question: {'is_deleted': question is None},
    )

    return fetched_questions
