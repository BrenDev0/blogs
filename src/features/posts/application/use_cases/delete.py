from uuid import UUID
from src.features.posts.domain import entities, schemas
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException

class DeleteBlogPost:
    def __init__(
        self,
        post_repository: data_repository.DataRepository
    ):
        self.__post_repository = post_repository

    def execute(
        self,
        user_id: UUID,
        post_id: UUID
    ): 
        post: entities.BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_post: entities.BlogPost = self.__post_repository.delete(
            key="post_id",
            value=post.post_id
        )

        return schemas.BlogPostPublic.model_validate(deleted_post, from_attributes=True)