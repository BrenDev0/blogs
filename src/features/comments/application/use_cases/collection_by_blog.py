from uuid import UUID
from typing import List, Union
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.comments.domain import entities, schemas, comment_repository
from src.features.posts.domain.entities import BlogPost

class CommentsCollection:
    def __init__(
        self,
        comment_repository: comment_repository.CommentRepository,
        post_repository: data_repository.DataRepository
    ):
        self.__comment_repository = comment_repository
        self.__post_repository = post_repository
        self.allowed_filters = ["approved"]
    def execute(
        self,
        user_id: UUID,
        per_page: int,
        page_number: int,
        scope: str,
        scope_id: UUID,
        filter_results: bool = False,
        filter: str = None,
        filter_value: Union[str, UUID, bool] = None
    ):
        offset = (page_number - 1) * per_page

        if scope.lower() == "post":
            pass


            

        
        
        
        
        
        
