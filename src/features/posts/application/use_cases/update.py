from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain import entities, schemas
from  datetime import datetime
from datetime import datetime, timezone

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
        cleaned_changes = changes.model_dump(exclude_none=True, by_alias=False)
        if not cleaned_changes:
            raise exceptions.UpdateFieldsException()
        
        post: entities.BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()
        

        is_publishing = cleaned_changes.get("published")
        
        if is_publishing:
            publishing_datetime = datetime.now(timezone.utc)
            cleaned_changes["published_at"] = publishing_datetime

        updated_post: entities.BlogPost = self.__post_repository.update(
            key="post_id",
            value=post_id,
            changes=cleaned_changes
        )

        return schemas.BlogPostPublic.model_validate(updated_post, from_attributes=True)