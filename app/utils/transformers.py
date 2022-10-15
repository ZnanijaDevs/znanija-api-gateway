import re
from app.constants import BRAINLY_SUBJECTS, DEFAULT_USER_AVATAR
from app.brainly_api import from_id
from app.models.users import TransformedGraphqlUser, TransformedLegacyUserWithBasicData
from . import filter_node_content


def get_subject_by_id(id: int) -> str:
    subject_id = str(id)

    for subject in BRAINLY_SUBJECTS:
        if subject['id'] == subject_id:
            return subject['name']


def transform_task_node(node: dict, users_data: list[dict]) -> dict:
    is_answer = 'responses' not in node
    node_settings = node['settings']
    node_content = node['content']

    filtered_content = filter_node_content(node_content)

    transformed_node = {
        'id': node['id'],
        'content': {
            'short': f"{filtered_content[:300]}..." if len(filtered_content) > 300 else filtered_content,
            'full': node_content,
            'filtered': filtered_content
        },
        'attachments': [attachment['full'] for attachment in node['attachments']],
        'is_reported': node_settings['is_marked_abuse'],
        'is_deleted': node_settings['is_deleted'],
        'has_attachments': len(node['attachments']) > 0,
        'created': node['created'],
    }

    if is_answer:
        transformed_node['is_approved'] = node_settings['is_confirmed']
        transformed_node['is_best'] = node['best']
    else:
        transformed_node['points'] = node['points']['ptsForTask']
        transformed_node['link'] = f"https://znanija.com/task/{node['id']}"
        transformed_node['subject'] = get_subject_by_id(node['subject_id'])

    # Find author
    author_user_id = node['user_id']
    for user in users_data:
        if user['id'] != author_user_id:
            continue

        transformed_node['author'] = {
            'avatar': user['avatars']['100'],
            'is_deleted': user['is_deleted'],
            'ranks': user['ranks']['names'],
            'id': author_user_id,
            'nick': user['nick']
        }

    return transformed_node


def transform_log_entry(entry: dict, users_data: list[dict]) -> dict:
    def find_user(id: int) -> dict:
        for user in users_data:
            if user['id'] != id:
                continue

            return {
                'id': user['id'],
                'nick': user['nick'],
                'ranks': user['ranks']['names']
            }

    owner = find_user(entry.get('owner_id'))
    user = find_user(entry.get('user_id'))

    entry_text = entry['text']

    if user:
        entry_text = entry_text.replace('%1$s', f"${user['nick']}-{user['id']}$")
    if owner:
        entry_text = re.sub(r"%\d\$\w*", f"${owner['nick']}-{owner['id']}$", entry_text)

    entry_descriptions = entry.get('descriptions') or []

    return {
        'text': entry_text,
        'warn': entry['warn'],
        'type': entry['class'],
        'time': entry['time'],
        'descriptions': [{
            'text': description['text'],
            'title': description['subject']
        } for description in entry_descriptions],
        'owner': owner,
        'user': user,
        'date': entry['date']
    }


def transform_legacy_user_with_basic_data(node: dict) -> TransformedLegacyUserWithBasicData:
    """Transform a legacy `User` with basic data only to a dict"""
    return {
        'nick': node['nick'],
        'id': node['id'],
        'is_deleted': node['is_deleted'],
        'avatar': node['avatar']['medium'] if node['avatar'] else None,
    }


def transform_gql_user(node: dict) -> TransformedGraphqlUser:
    """Transform a GraphQL type `User` to a dict"""
    user = TransformedGraphqlUser(
        id=from_id(node['id']),
        nick=node['nick'],
        avatar=node['avatar']['url'] if node['avatar'] else DEFAULT_USER_AVATAR,
        rank=node['rank']['name'] if node['rank'] else None,
        created=node['created'],
    )

    # Calculate user answers
    answer_count_by_subject: list[dict[str, dict | int]] = node.get('answerCountBySubject')
    answers_count = 0

    for count in answer_count_by_subject:
        answers_count += count['count']

        count['subject'] = count['subject']['name']

    user.has_special_ranks = len(node.get('specialRanks') or []) > 0
    user.answers_count = answers_count
    user.answers_count_by_subject = answer_count_by_subject

    return user
