import logging
import strawberry
from uuid import UUID
from typing import List, Optional
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
        description="Get all posts by blog id. perPage: # of results returned defualt will be 10, pageNumber: current page the user is requesting, categoryId: Optional, if included the results will be filtered by the category id given"
    )
    def private_collection(
        self,
        blog_id: UUID,
        page_number: int,
        info: strawberry.Info,
        category_id: Optional[UUID] = None,
        per_page: Optional[int] = 10
    ) -> List[types.BlogPostType]:
        user_id = info.context.get("user_id")
        use_case = get_blog_post_collection_use_case()
        try:
            if category_id:
                return use_case.execute(
                    user_id=user_id,
                    blog_id=blog_id,
                    category_id=category_id,
                    per_page=per_page,
                    page_number=page_number,
                    include_drafts=True
                )
            
            else:
                return use_case.execute(
                    user_id=user_id,
                    blog_id=blog_id,
                    per_page=per_page,
                    page_number=page_number,
                    include_drafts=True
                )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.field(
        description="**UNPROTECTED**, Public endpoint Get published posts by blog id. perPage: # of results returned defualt will be 10, pageNumber: current page the user is requesting, categoryId: Optional, if included the results will be filtered by the category id given"
    )
    def public_collection(
        self,
        blog_id: UUID,
        page_number: int,
        category_id: Optional[UUID] = None,
        per_page: Optional[int] = 10
    ) -> List[types.BlogPostType]:
        use_case = get_blog_post_collection_use_case()
        try:
            if category_id:
                return use_case.execute(
                    blog_id=blog_id,
                    category_id=category_id,
                    per_page=per_page,
                    page_number=page_number,
                    include_drafts=False
                )
            
            else:
                return use_case.execute(
                    blog_id=blog_id,
                    per_page=per_page,
                    page_number=page_number,
                    include_drafts=False
                )
        
        except PermissionsException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()