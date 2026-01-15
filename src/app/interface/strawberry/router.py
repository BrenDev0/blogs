import logging
from strawberry.fastapi import GraphQLRouter
from src.app.interface.strawberry.schema import schema
logger = logging.getLogger(__name__)


def get_strawberry_graphql_router():
    if schema is None:
        raise ValueError("GraphQL schema cannot be None")
    
    return GraphQLRouter(
        schema,
        path="/graphql",
        multipart_uploads_enabled=True
    )