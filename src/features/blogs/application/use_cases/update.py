from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.blogs.domain import schemas, entities

class UpdateBlog:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        changes: schemas.UpdateBlogRequest
    ):
        cleaned_changes = changes.model_dump(exclude_none=True, by_alias=False)
        if not cleaned_changes:
            raise exceptions.UpdateFieldsException()
        
        blog: entities.Blog = self.__repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise exceptions.NotFoundException("Blog not found")
        
        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_blog: entities.Blog = self.__repository.update(
            key="blog_id",
            value=blog.blog_id,
            changes=cleaned_changes
        )

        return schemas.BlogPublic.model_validate(updated_blog, from_attributes=True)