from fastapi import APIRouter

from app.brainly_api import graphql_api
from app.brainly_api.graphql_queries import GET_FEED_QUERY
from app.utils.transformers import transform_gql_feed_node
from app.models import GetFeedResponse


router = APIRouter(prefix='/brainly/feed')


@router.get('', response_model=GetFeedResponse, response_model_exclude_none=True)
async def get_feed(cursor: str | None = None):
    data = await graphql_api.query(GET_FEED_QUERY, {
        'before': cursor
    })

    return GetFeedResponse(
        end_cursor=data['feed']['pageInfo']['endCursor'],
        nodes=[
            transform_gql_feed_node(edge['node']) for edge in data['feed']['edges']
        ]
    )
