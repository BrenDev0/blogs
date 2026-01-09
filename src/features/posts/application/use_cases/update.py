from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain import entities, schemas

class UpdateBlogPost:
    def __init__(
        self,
        post_repository: data_repository.DataRepository
    ):
        self.__post_repository = post_repository

    def execute(
        self,
        user_id: UUID,
        post_id: UUID,
        changes: schemas.UpdateBlogPostRequest
    ): 
        post: entities.BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_post: entities.BlogPost = self.__post_repository.update(
            key="post_id",
            value=post_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return schemas.BlogPostPublic.model_validate(updated_post, from_attributes=True)