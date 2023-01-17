from .legacy import LegacyApi
from .graphql import GraphqlApi
from .legacy_pages import send_form, get_parsed_page, get_form_data_from_user_page
from .transform_id import to_id, from_id
from .content_classification.get_reported_content_count import get_reported_content_count


legacy_api = LegacyApi()
graphql_api = GraphqlApi()


__all__ = [
    "legacy_api",
    "graphql_api",
    "send_form",
    "get_parsed_page",
    "get_form_data_from_user_page",
    "get_reported_content_count",
    "to_id",
    "from_id"
]
