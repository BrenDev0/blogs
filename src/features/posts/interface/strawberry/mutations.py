import logging
import strawberry
from uuid import UUID
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.posts.interface.strawberry import types, inputs
from src.features.posts.dependencies.use_cases import (
    get_create_blog_post_use_case,
    get_delete_blog_post_use_case,
    get_update_blog_post_use_case
)
logger = logging.getLogger(__name__)

@strawberry.type
class BlogPostMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create a blog post"
    )
    def create_blog_post(
        self,
        blog_id: UUID,
        info: strawberry.Info,
        input: inputs.CreateBlogPostInput
    ) -> types.BlogPostType:
        user_id = info.context.get("user_id")
        use_case = get_create_blog_post_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                blog_id=blog_id,
                req_data=input.to_pydantic()
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update blog post by id"
    )
    def update_blog_post(
        self,
        post_id: UUID,
        info: strawberry.Info,
        input: inputs.UpdateBlogPostInput
    ) -> types.BlogPostType:
        user_id = info.context.get("user_id")
        use_case = get_update_blog_post_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                post_id=post_id,
                changes=input.to_pydantic()
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete blog post by id"
    )
    def delete_blog_post(
        self,
        post_id: UUID,
        info: strawberry.Info
    ) -> types.BlogPostType:
        user_id = info.context.get("user_id")
        use_case = get_delete_blog_post_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                post_id=post_id
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()