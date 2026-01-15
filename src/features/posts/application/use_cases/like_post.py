from uuid import UUID
from src.persistence.domain import exceptions, data_repository
from src.features.posts.domain import entities, schemas

class LikePost:
    def __init__(
        self,
        post_repository: data_repository.DataRepository
    ):
        self.__post_repository = post_repository

    def execute(
        self,
        post_id: UUID
    ):
        post: entities.BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        likes = post.likes + 1
        changes = {
            "likes": int(likes)
        }

        self.__post_repository.update(
            key="post_id",
            value=post.post_id,
            changes=changes
        )

        return
