import logging
import strawberry
from uuid import UUID
from typing import List
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.security.domain.exceptions import PermissionsException
from src.features.posts.interface.strawberry import types
from src.features.posts.dependencies.use_cases import get_blog_post_collection_use_case
logger = logging.getLogger(__name__)

@strawberry.type
class BlogPostQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get all posts by blog id"
    )
    def collection_all_posts(
        self,
        blog_id: UUID,
        info: strawberry.Info
    ) -> List[types.BlogPostType]:
        user_id = info.context.get("user_id")
        use_case = get_blog_post_collection_use_case()
        try:
            return use_case.execute(
                user_id=user_id,
                blog_id=blog_id,
                include_drafts=True
            )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.field(
        description="Get all published posts by blog id, **UNPROTECTED**"
    )
    def collection_all_published_posts(
        self,
        blog_id: UUID
    ) -> List[types.BlogPostType]:
        use_case = get_blog_post_collection_use_case()
        try:
            return use_case.execute(
                blog_id=blog_id,
                include_drafts=False
            )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()