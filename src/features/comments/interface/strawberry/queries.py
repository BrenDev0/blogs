import strawberry
from uuid import UUID
from typing import List
import logging
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.comments.interface.strawberry.types import CommentType
from src.features.comments.dependencies.use_cases import get_comment_collection_use_case
logger = logging.getLogger(__name__)

@strawberry.type
class CommentQueries:
    @strawberry.field(
        description=
        """
        Get all approved comments. **UPROTECTED**
        """
    )
    def public_collection(
        post_id: UUID
    ) -> List[CommentType]:
        try:
            use_case = get_comment_collection_use_case()

            return use_case.execute(
                post_id=post_id,
                include_unapproved=False
            )
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.field(
        permission_classes=[UserAuth],
        description=
        """
        Get all comments.
        """
    )
    def public_collection(
        post_id: UUID,
        info: strawberry.Info
    ) -> List[CommentType]:
        try:
            user_id = info.context.get("user_id")
            use_case = get_comment_collection_use_case()

            return use_case.execute(
                post_id=post_id,
                user_id=user_id,
                include_unapproved=True
            )
        
        except PermissionError as e:
            raise GraphQlException(e)

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()