import strawberry
import logging
from uuid import UUID
from typing import List
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.app.domain.exceptions import GraphQlException
from src.features.blogs.dependencies.use_cases import (
    get_blog_resource_use_case,
    get_blogs_collection_use_case
)
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.features.blogs.interface.strawberry.types import BlogType
logger = logging.getLogger(__name__)

@strawberry.type
class BlogQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get blog by id"
    )
    def blog_resource(
        self,
        info: strawberry.Info,
        blog_id: UUID
    ) -> BlogType:
        user_id = info.context.get("user_id")
        use_case = get_blog_resource_use_case()

        try: 
            return use_case.execute(
                user_id=user_id,
                blog_id=blog_id
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get blogs by user"
    )
    def blogs_collection(
        self,
        info: strawberry.Info
    )-> List[BlogType]:
        user_id = info.context.get("user_id")
        use_case = get_blogs_collection_use_case()

        try:
            return use_case.execute(
                user_id=user_id
            )
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()