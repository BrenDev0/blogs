from uuid import UUID
from typing import List
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

    def execute(
        self,
        post_id: UUID,
        user_id: UUID = None,
        include_unapproved: bool = False  
    ):
        comments: List[entities.Comment] = self.__comment_repository.get_many(
            key="post_id",
            value=post_id
        )

        if not comments:
            return []

        if include_unapproved:
            if not user_id:
                raise ValueError("User id required to query all comments")
            
            post: BlogPost = self.__post_repository.get_one(
                key="post_id",
                value=post_id
            )

            if not post:
                for comment in comments:
                    self.__comment_repository.delete(
                        key="comment_id",
                        value=comment.comment_id
                    )

                raise exceptions.NotFoundException("Comments unavailbale")
            
            if str(post.blog.user_id) != str(user_id):
                raise PermissionsException()

            return [
                schemas.CommentPublic.model_validate(comment, from_attributes=True) for comment in comments 
            ]
        
        else:
            return [
                schemas.CommentPublic.model_validate(comment, from_attributes=True) for comment in comments if comment.approved
            ]
