import strawberry
import logging
from  uuid import UUID
from src.persistence.domain.exceptions import NotFoundException, UpdateFieldsException
from src.security.domain.exceptions import PermissionsException
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.features.categories.dependencies.use_cases import (
    get_delete_category_use_case,
    get_create_category_use_case,
    get_update_category_use_case
)
from src.features.categories.interface.strawberry import types, inputs
logger = logging.getLogger(__name__)

@strawberry.type
class CategoryMutation:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create a category"
    )
    @validate_input_to_model
    def create_category(
        self,
        blog_id: UUID,
        info: strawberry.Info,
        input: inputs.CreateCategoryInput
    ) -> types.CategoryType:
        user_id = info.context.get("user_id")
        use_case = get_create_category_use_case()
        
        try:
            return use_case.execute(
                blog_id=blog_id,
                user_id=user_id,
                req_data=input
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update category by id"
    )
    @validate_input_to_model
    def update_category(
        self,
        info: strawberry.Info,
        category_id: UUID,
        input: inputs.UpdateCategoryInput
    )-> types.CategoryType:
        user_id = info.context.get("user_id")
        use_case = get_update_category_use_case()
    
        try:
            return use_case.execute(
                user_id=user_id,
                category_id=category_id,
                changes=input
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete category by id"
    )
    def delete_category(
        self,
        info: strawberry.Info,
        category_id: UUID
    )-> types.CategoryType:
        user_id = info.context.get("user_id")
        use_case = get_delete_category_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                category_id=category_id
            )
        
        except (PermissionsException, NotFoundException, UpdateFieldsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()