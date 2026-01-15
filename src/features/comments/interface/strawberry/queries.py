import strawberry
from uuid import UUID
from typing import List, Optional, Annotated, Union
import logging
import json
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import InvalidFilterException, InvalidScopeException, PagationException
from src.security.domain.exceptions import PermissionsException
from src.features.comments.interface.strawberry import types, inputs
from src.features.comments.dependencies.use_cases import get_comment_collection_use_case
logger = logging.getLogger(__name__)


@strawberry.type
class StringValue:
    value: str

@strawberry.type
class IntValue:
    value: int

@strawberry.type
class BoolValue:
    value: bool

@strawberry.type
class UUIDVAlue:
    value: UUID

FilterValueUnion = Annotated[
    Union[str,int, bool],
    strawberry.union("FilterValueUnion")
]




@strawberry.type
class CommentQueries:
    @strawberry.field(
        description=
        """
        Get all approved comments. **UPROTECTED**
        """
    )
    def public_collection(
        post_id: UUID,
        page_number: int, 
        per_page: int = 10,
        
    ) -> List[types.CommentType]:
        try:
            use_case = get_comment_collection_use_case()

            return use_case.execute(
                scope="post",
                scope_id=post_id,
                page_number=page_number,
                per_page=per_page,
                protected=False
            )
        
        except PagationException as e:
            raise GraphQlException(str(e))
        
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
    def private_collection(
        info: strawberry.Info,
        scope: str,
        scope_id: UUID,
        page_number: int,
        per_page: Optional[int] = 10,
        filter_results: Optional[bool] = False,
        filter: Optional[str] = None,
        filter_value: Optional[strawberry.scalars.JSON] = None
    ) -> List[types.CommentType]:
        try:
            user_id = info.context.get("user_id")
            use_case = get_comment_collection_use_case()
  
            return use_case.execute(
                per_page=per_page,
                page_number=page_number,
                scope=scope,
                scope_id=scope_id,
                user_id=user_id,
                protected=True,
                filter_results=filter_results,
                filter=filter,
                filter_value=filter_value
            )
            
        
        except (PermissionError, InvalidScopeException, InvalidFilterException, PagationException) as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        