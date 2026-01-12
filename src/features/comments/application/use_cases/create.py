from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.comments.domain import entities, schemas


class CreateComment:
    def __init__(
        self,
        comment_repository: data_repository.DataRepository,
        post_repository: data_repository.DataRepository
    ):
        self.__comment_repostiory = comment_repository
        self.__post_repository = post_repository

    def execute(
        self,
        post_id: UUID,
        comment: schemas.CreateCommentRequest
    ):
        post = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        

        data = entities.Comment(
            **comment.model_dump(exclude_none=True),
            approved=False
        )

        new_comment = self.__comment_repostiory.create(data=data)

        return schemas.CommentPublic.model_validate(new_comment, from_attributes=True)
    