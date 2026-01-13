from uuid import UUID
from typing import List
from src.persistence.domain import exceptions, data_repository
from src.security.domain.exceptions import PermissionsException
from src.features.comments.domain import entities, schemas, comment_repository
from src.features.posts.domain.entities import BlogPost

class ApproveAllComments:
    def  __init__(
        self,
        comment_repository: comment_repository.CommentRepository,
        post_repository: data_repository.DataRepository
    ):
        self.__comment_repository = comment_repository
        self.__post_repository = post_repository

    
    def execute(
        self,
        post_id: UUID,
        user_id: UUID
    ):
        post: BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()
        
        changes = {
            "approved": True
        }
        updated_comments: List[entities.Comment] = self.__comment_repository.update_many(
            key="post_id",
            value=post.post_id,
            changes=changes
        )

        return [
            schemas.CommentPublic.model_validate(comment, from_attributes=True) for comment in updated_comments
        ]

