from fastapi import APIRouter

from app.brainly_api import graphql_api
from app.brainly_api.graphql_queries import GET_FEED_QUERY
from app.utils.transformers import transform_gql_feed_node


router = APIRouter(prefix='/brainly/feed')


@router.get('', response_model_exclude_none=True)
async def get_feed():
    data = await graphql_api.query(GET_FEED_QUERY)

    edges = []

    for edge in data['feed']['edges']:
        edges.append(transform_gql_feed_node(edge['node']).dict(exclude_none=True))

    return {
        'edges': edges,
        'end_cursor': data['feed']['pageInfo']['endCursor'],
    }
