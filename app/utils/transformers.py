import re
from app.constants import BRAINLY_SUBJECTS, DEFAULT_USER_AVATAR, DELETED_USER_DATA, DELETED_ACCOUNT_NICK
from app.brainly_api import from_id
from app.models import TransformedGraphqlUser, LegacyUserWithBasicData, \
    FeedNode, EntryInTaskLog, LegacyUser, LegacyQuestion, LegacyAnswer
from . import filter_node_content


def get_subject_by_id(id: int) -> str:
    """Get Brainly subject by id"""
    subject_id = str(id)

    for subject in BRAINLY_SUBJECTS:
        if subject["id"] == subject_id:
            return subject["name"]


def transform_task_log_entries(entries: list[dict], users_data: list[dict]) -> list[EntryInTaskLog]:
    """Transform log entries to a list of EntryInTaskLog classes"""
    def find_user(id: int) -> dict:
        for user in users_data:
            if user["id"] != id:
                continue

            return transform_legacy_user(user)

    transformed_entries: list[EntryInTaskLog] = []

    for entry in entries:
        owner = find_user(entry.get("owner_id"))
        user = find_user(entry.get("user_id"))

        entry_text = entry["text"]

        if user:
            entry_text = entry_text.replace("%1$s", f"${user.nick}-{user.id}$")
        if owner:
            entry_text = re.sub(r"%\d\$\w*", f"${owner.nick}-{owner.id}$", entry_text)

        entry_descriptions = entry.get("descriptions") or []

        transformed_entries.append(EntryInTaskLog(
            text=entry_text,
            warn=entry["warn"],
            type=entry["class"],
            time=entry["time"],
            owner=owner,
            user=user,
            date=entry["date"],
            descriptions=[{
                "text": description["text"],
                "title": description["subject"]
            } for description in entry_descriptions]
        ))

    return transformed_entries


def transform_legacy_user_with_basic_data(node: dict) -> LegacyUserWithBasicData:
    """Transform a legacy User with basic data only to LegacyUserWithBasicData class"""
    return LegacyUserWithBasicData(
        nick=node["nick"],
        id=node["id"],
        is_deleted=node["is_deleted"],
        avatar=node["avatar"]["medium"] if node["avatar"] else None
    )


def transform_legacy_user(node: dict) -> LegacyUser:
    """Transform a legacy User to a LegacyUser class"""
    return LegacyUser(
        id=node["id"],
        nick=node["nick"],
        is_deleted=node["nick"] == DELETED_ACCOUNT_NICK,
        avatar=node["avatars"]["100"] if node["avatars"] is not None else None,
        gender=node["gender"],
        ranks=node["ranks"]["names"]
    )


def transform_gql_user(node: dict) -> TransformedGraphqlUser:
    """Transform a GraphQL type User to a dict"""
    if node is None:  # user is deleted
        return TransformedGraphqlUser(**DELETED_USER_DATA)

    user = TransformedGraphqlUser(
        id=from_id(node["id"]),
        nick=node["nick"],
        avatar=node["avatar"]["url"] if node["avatar"] else DEFAULT_USER_AVATAR,
        rank=node["rank"]["name"] if node["rank"] else None,
        created=node["created"],
        gender=node["gender"],
        special_ranks=[rank["name"] for rank in node["specialRanks"]],
        is_deleted=False
    )

    # Calculate user answers
    answer_count_by_subject: list[dict[str, dict | int]] = node.get("answerCountBySubject")
    answers_count = 0

    if answer_count_by_subject is not None:
        for count in answer_count_by_subject:
            answers_count += count["count"]

            count["subject"] = count["subject"]["name"]

        user.answers_count_by_subject = answer_count_by_subject

    user.has_special_ranks = len(node.get("specialRanks") or []) > 0
    user.answers_count = answers_count

    return user


def transform_gql_feed_node(node: dict) -> FeedNode:
    """Transform a GraphQL type Question/Answer from the feed query to FeedNode"""
    transformed_node = FeedNode(
        content=filter_node_content(node["content"]),
        is_reported=node["moderationItem"] is not None,
        created=node["created"],
        id=from_id(node["id"]),
        author=transform_gql_user(node["author"]) if node["author"] is not None else None,
        attachments=[attachment["url"] for attachment in node["attachments"]]
    )

    if "answers" in node:  # node is `Question`
        transformed_node.subject = node["subject"]["name"]
        transformed_node.subject_id = from_id(node["subject"]["id"])
        transformed_node.answers = [
            transform_gql_feed_node(answer) for answer in node["answers"]["nodes"]
        ]
    else:  # node is `Answer`
        transformed_node.is_confirmed = node["isConfirmed"]
        transformed_node.is_best = node["isBest"]

    return transformed_node


def transform_task_node(node: dict, users_data: list[dict]) -> dict:
    """Transform a node in the task data to a dict"""
    is_answer = "responses" not in node
    node_settings = node["settings"]
    node_content = node["content"]

    filtered_content = filter_node_content(node_content)

    transformed_node = {
        "id": node["id"],
        "attachments": [attachment["full"] for attachment in node["attachments"]],
        "is_reported": node_settings["is_marked_abuse"],
        "is_deleted": node_settings["is_deleted"],
        "has_attachments": len(node["attachments"]) > 0,
        "created": node["created"],
        "full_content": node_content,
        "filtered_content": filtered_content,
        "short_content": f"{filtered_content[:300]}..." if len(filtered_content) > 300 else filtered_content,
    }

    if is_answer:
        transformed_node["is_approved"] = node_settings["is_confirmed"]
        transformed_node["is_best"] = node["best"]
        transformed_node["is_to_correct"] = node_settings["is_to_correct"]
    else:
        transformed_node["points"] = node["points"]["ptsForTask"]
        transformed_node["link"] = f"https://znanija.com/task/{node['id']}"
        transformed_node["can_answer"] = node_settings["is_answer_button"]
        transformed_node["subject"] = get_subject_by_id(node["subject_id"])
        transformed_node["subject_id"] = node["subject_id"]

    # Find author
    author_id = node["user_id"]
    for user in users_data:
        if user["id"] == author_id:
            transformed_node["author"] = transform_legacy_user(user)
            break

    return transformed_node


def transform_task(node: dict, users_data: list[dict]) -> LegacyQuestion:
    """Transform a legacy task data to a LegacyQuestion class"""
    task = node["task"]
    responses = node["responses"]

    return LegacyQuestion(
        **transform_task_node(task, users_data),
        answers=[
            LegacyAnswer(**transform_task_node(response, users_data)) for response in responses
        ],
        answers_count=len(responses)
    )
