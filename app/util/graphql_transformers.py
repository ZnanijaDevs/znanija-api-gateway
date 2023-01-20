from app.constants import DEFAULT_USER_AVATAR, DELETED_USER_DATA
from app.brainly_api import from_id
from app.models import TransformedGraphqlUser, FeedNode
from .common import filter_node_content


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
