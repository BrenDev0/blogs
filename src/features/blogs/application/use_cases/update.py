from uuid import UUID
from src.persistence.domain.repositories import DataRepository
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.blogs.domain.schemas import BlogPublic, UpdateBlogRequest
from src.features.blogs.domain.entities import Blog

class UpdateBlog:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        changes: UpdateBlogRequest
    ):
        blog: Blog = self.__repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise NotFoundException("Blog not found")
        
        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_blog: Blog = self.__repository.update(
            key="blog_id",
            value=blog.blog_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return BlogPublic.model_validate(updated_blog, from_attributes=True)