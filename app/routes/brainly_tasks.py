from fastapi import APIRouter

from app.models import BRAINLY_ID, CheckDeletedTasksPayload
from app.brainly_api import legacy_api, graphql_api
from app.brainly_api.exceptions import QuestionDoesNotExistException
from app.utils import to_id
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
    task_ids = payload.ids

    if len(task_ids) == 0:
        return []

    query = ''
    for task_id in task_ids:
        query += f"q_{task_id}: question(id: \"{to_id(task_id, 'question')}\")" + "{id} "

    response = await graphql_api.query('query {' + query + ' }')
    fetched_questions = response['data']

    questions = [{
        'id': int(key.split('_').pop()),
        'is_deleted': fetched_questions[key] is None
    } for key in fetched_questions.keys()]

    return questions
