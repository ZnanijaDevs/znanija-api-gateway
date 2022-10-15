from typing import Any, Callable

from .api import Api
from .exceptions import BrainlyAPIRequestGeneralException
from .transform_id import to_id


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
            {'query': query.strip(), 'variables': variables}
        )

        if 'errors' in r:
            raise BrainlyAPIRequestGeneralException(r['errors'], 'graphql')

        return r['data']

    async def mapped_query_with_ids(
        self,
        ids: list[int],
        map_prefix: str,
        body: str,
        transform_entry: Callable[dict, dict],
        extra_query: str = ''
    ) -> list[dict]:
        """Make a mapped GraphQL query"""
        if len(ids) == 0:
            return []

        query = extra_query + ' query {'
        for id in ids:
            query += f"_{id}: {map_prefix}(id: \"{to_id(id, map_prefix)}\") " + '{' + body + '} '

        query += ' }'

        data = await self.query(query)
        results = []

        for key, item in data.items():
            transformed_entry = transform_entry(item)

            if isinstance(transformed_entry, dict):
                transformed_entry['id'] = int(key.replace('_', ''))

            results.append(transformed_entry)

        return results

graphql_api = GraphqlApi()
