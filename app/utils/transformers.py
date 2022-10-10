import re
from app.constants import BRAINLY_SUBJECTS


def get_subject_by_id(id: int) -> str:
    subject_id = str(id)

    for subject in BRAINLY_SUBJECTS:
        if subject['id'] == subject_id:
            return subject['name']


def transform_task_node(node: dict, users_data: list[dict]) -> dict:
    is_answer = 'responses' not in node
    node_settings = node['settings']
    node_content = node['content']

    # Replace words
    filtered_content = node_content
    replacements = [(r"<\/?\w+\s?\/?>", ''), (r"\n{2,}", '\n'), (r"^(\s|\n)|(\s?\n)$", '')]
    for regex, new in replacements:
        filtered_content = re.sub(regex, new, filtered_content)

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
