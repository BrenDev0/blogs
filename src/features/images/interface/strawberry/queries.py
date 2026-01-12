import logging
import strawberry
from uuid import UUID
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.app.domain.exceptions import GraphQlException
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.images.interface.strawberry import types
from src.features.images.dependencies.use_cases import get_image_collection_use_case
logger = logging.getLogger(__name__)

@strawberry.type
class ImageQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Gets images for any post, this route is protected to allow only user accounts to get images for posts not yet published"
    )
    def image_collection_any(
        self,
        post_id: UUID,
        info: strawberry.Info
    ) -> types.ImageType:
        user_id = info.context.get("user_id")
        use_case = get_image_collection_use_case()

        try:
            return use_case.execte(
                user_id=user_id,
                post_id=post_id,
                include_drafts=True
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.field(
        description="Gets images for a published post, this route is public to allow anyone to get images for published posts only, **UNPROTECTED**"
    )
    def image_collection_published(
        self,
        post_id: UUID,
    ) -> types.ImageType:
        use_case = get_image_collection_use_case()

        try:
            return use_case.execte(
                post_id=post_id,
                include_drafts=False
            )
        
        except (NotFoundException, PermissionsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()