from uuid import UUID
from typing import List, Union, Any
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.comments.domain import entities, schemas, comment_repository
from src.features.posts.domain.entities import BlogPost
from src.types.application.services.type_validation import TypeValidationService

class CommentsCollection:
    def __init__(
        self,
        comment_repository: comment_repository.CommentRepository,
        post_repository: data_repository.DataRepository,
        type_validation_service: TypeValidationService
    ):
        self.__comment_repository = comment_repository
        self.__post_repository = post_repository
        self.__type_validation_service = type_validation_service
        self.allowed_filters = {"approved": bool}
        self.allowed_scopes = ["blog", "post"]        

    def __validate_filters(
        self,
        filter: str,
        filter_value

    ):
        if filter not in self.allowed_filters:
            available = ', '.join(self.allowed_filters.keys())
            raise exceptions.InvalidFilterException(
                f"Filter '{filter}' not available. Available: {available}"
            )
        

        try:
            valid_filter_value = self.__type_validation_service.validate(
                expected_type=self.allowed_filters[filter.lower()].__name__,
                value_to_check=filter_value
            )

            return valid_filter_value
        

        except ValueError as e:
            raise exceptions.InvalidFilterException(str(e))
    

    def execute(
        self,
        per_page: int,
        page_number: int,
        scope: str,
        scope_id: UUID,
        user_id: UUID = None,
        protected: bool = True,
        filter_results: bool = False,
        filter: str = None,
        filter_value: Union[str, UUID, bool] = None
    ):
        if scope not in self.allowed_scopes:
            raise exceptions.InvalidScopeException(f"Scope {scope} not  allowed. Available")
        
        if page_number < 1:
            raise exceptions.PagationException("Page number cannot be lower than 1")

        offset = (page_number - 1) * per_page

        if not protected:
            comments = self.__comment_repository.get_many(
                key="post_id",
                value=scope_id,
                limit=per_page,
                offset=offset,
                secondary_key="approved",
                secondary_value=True
            )
        else: 
            if not user_id:
                raise ValueError("User id required for protected content")
                    
            if scope.lower() == "post":
                post: BlogPost = self.__post_repository.get_one(
                    key="post_id",
                    value=scope_id
                )

                if str(post.blog.user_id) != str(user_id):
                    raise PermissionsException()
            
                if filter_results:
                    valid_filter_value = self.__validate_filters(filter=filter, filter_value=filter_value)
                    
                    comments = self.__comment_repository.get_many(
                        key="post_id",
                        value=scope_id,
                        limit=per_page,
                        offset=offset,
                        secondary_key=filter,
                        secondary_value=valid_filter_value
                    )

                else: 
                    comments = self.__comment_repository.get_many(
                        key="post_id",
                        value=scope_id,
                        limit=per_page,
                        offset=offset
                    )
            else:
                all_posts: List[BlogPost] = self.__post_repository.get_many(
                    key="blog_id",
                    value=scope_id
                )
                if filter_results:
                    valid_filter_value = self.__validate_filters(filter=filter, filter_value=filter_value)

                    comments = self.__comment_repository.get_many(
                        key="post_id",
                        value=[
                            post.post_id for post in all_posts
                        ],
                        limit=per_page,
                        offset=offset,
                        secondary_key=filter,
                        secondary_value=valid_filter_value
                    )
                
                else:
                    comments = self.__comment_repository.get_many(
                        key="post_id",
                        value=[
                            post.post_id for post in all_posts
                        ],
                        limit=per_page,
                        offset=offset
                    )
        
        return [
            schemas.CommentPublic.model_validate(comment, from_attributes=True) for comment in comments
        ]
        
        
            
            
