from .legacy import LegacyApi
from .graphql import GraphqlApi
from .legacy_pages import send_form, get_parsed_page, get_form_data_from_user_page
from .transform_id import to_id, from_id

legacy_api = LegacyApi()
graphql_api = GraphqlApi()
