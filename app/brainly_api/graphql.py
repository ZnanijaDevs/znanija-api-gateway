from typing import Any

from .api import Api
from .exceptions import BrainlyAPIRequestGeneralException


class GraphqlApi(Api):
    """
    Class that represents Brainly GraphQL API.
    The legacy API will be replaced with GraphQL in the future.
    """
    async def query(
        self,
        query: str,
        variables: Any | None = None
    ) -> dict:
        """Execute a GraphQL query"""
        r = await self._make_request(
            self.graphql_api_url,
            'POST',
            {'query': query, 'variables': variables}
        )

        if 'errors' in r:
            raise BrainlyAPIRequestGeneralException(r['errors'], 'graphql')

        return r

graphql_api = GraphqlApi()
