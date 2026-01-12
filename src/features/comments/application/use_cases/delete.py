from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.comments.domain import entities, schemas
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain.entities import BlogPost
class ApproveComment:
    def __init__(
        self,
        comment_repository: data_repository.DataRepository,
        post_repository: data_repository.DataRepository
    ):
        self.__comment_repository = comment_repository
        self.__post_repository = post_repository

    def execute(
        self,
        user_id: UUID,
        comment_id: UUID
    ):
        comment: entities.Comment = self.__comment_repository.get_one(
            key="comment_id",
            value=comment_id
        )

        if not comment:
            raise exceptions.NotFoundException("Comment not found")
        
        
        post: BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=comment.post_id
        )

        if not post:
            self.__comment_repository.delete(
                key=comment_id,
                value=comment.comment_id
            )

            raise exceptions.NotFoundException("Comment unavailable")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()

        deleted_comment: entities.Comment = self.__comment_repository.delete(
            key="comment_id",
            value=comment.comment_id
        )

        return schemas.CommentPublic.model_validate(deleted_comment, from_attributes=True)