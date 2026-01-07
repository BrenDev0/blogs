from uuid import UUID
from src.persistence.domain import repositories, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.blogs.domain import schemas, entities

class UpdateBlog:
    def __init__(
        self,
        repository: repositories.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        changes: schemas.UpdateBlogRequest
    ):
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
            changes=changes.model_dump(exclude_none=True)
        )

        return schemas.BlogPublic.model_validate(updated_blog, from_attributes=True)