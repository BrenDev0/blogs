import logging
import strawberry
from uuid import UUID
from src.app.domain.exceptions import GraphQlException
from src.features.blogs.interface.strawberry import (
    inputs,
    types
)
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.features.blogs.dependencies.use_cases import (
    get_create_blog_use_case,
    get_delete_blog_use_case,
    get_update_blog_use_case
)
from src.persistence.domain.exceptions import NotFoundException, UpdateFieldsException
from src.security.domain.exceptions import PermissionsException
logger = logging.getLogger(__name__)

@strawberry.type
class BlogMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create Blog"
    )
    @validate_input_to_model
    def create_blog(
        self,
        info: strawberry.Info,
        input: inputs.CreateBlogInput
    ) -> types.BlogType:
        user_id = info.context.get("user_id")
        use_case = get_create_blog_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                req_data=input
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete blog by id"
    )
    
    def delete_blog(
        self,
        info: strawberry.Info,
        blog_id: UUID
    ) -> types.BlogType:
        user_id = info.context.get("user_id")
        use_case = get_delete_blog_use_case()
        try:
            return use_case.execute(
                user_id=user_id,
                blog_id=blog_id
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update blog by id"
    )
    @validate_input_to_model
    def update_blog(
        self,
        info: strawberry.Info,
        blog_id: UUID,
        input: inputs.UpdateBlogInput
    ) -> types.BlogType:
        user_id = info.context.get("user_id")
        use_case = get_update_blog_use_case()
        
        try:
            return use_case.execute(
                user_id=user_id,
                blog_id=blog_id,
                changes=input
            )
        
        except (NotFoundException, PermissionError, UpdateFieldsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()