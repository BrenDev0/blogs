import strawberry
import logging
from uuid import UUID
from typing import List
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.comments.dependencies.use_cases import (
    get_approve_all_comments_use_case,
    get_approve_comment_use_case,
    get_create_comment_use_case,
    get_delete_comment_use_case
)
from src.features.comments.interface.strawberry import inputs, types
logger = logging.getLogger(__name__)

@strawberry.type
class CommentMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description=
        """
        Create comment, 
        comment will automatically be set to unapproved,
        **UNPROTECTED**
        """
    )
    @validate_input_to_model
    def public_create_comment(
        self,
        post_id: UUID,
        input: inputs.CreateCommentInput
    ) -> types.CommentType:
        try:
            use_case = get_create_comment_use_case()

            return use_case.execute(
                post_id=post_id,
                comment=input
            )
        
        except NotFoundException as e:
            raise 
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description=
        """
        Delete comment by id.
        """
    )
    def delete_comment(
        self,
        comment_id: UUID,
        info: strawberry.Info
    ) -> types.CommentType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_delete_comment_use_case()

            return use_case.execute(
                user_id=user_id,
                comment_id=comment_id
            )
        
        except (NotFoundException, PermissionError) as e:
            raise GraphQlException(str(e))
        
        except Exception as e: 
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description=
        """
        Approve comment by id.
        """
    )
    def approve_comment(
        self,
        comment_id: UUID,
        info: strawberry.Info
    ) -> types.CommentType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_approve_comment_use_case()

            return use_case.execute(
                user_id=user_id,
                comment_id=comment_id
            )
        
        except (NotFoundException, PermissionError) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()

    @strawberry.mutation(
        permission_classes=[UserAuth],
        description=
        """
        Approve all Comments
        """
    )
    def approve_all_comments(
        self,
        post_id: UUID,
        info: strawberry.Info
    ) -> List[types.CommentType]:
        try:
            user_id = info.context.get("user_id")
            use_case = get_approve_all_comments_use_case()

            return use_case.execute(
                post_id=post_id,
                user_id=user_id
            )
        
        except (NotFoundException, PermissionError) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()


