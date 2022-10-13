from .legacy import LegacyApi
from .graphql import GraphqlApi
from .transform_id import to_id, from_id

legacy_api = LegacyApi()
graphql_api = GraphqlApi()
