from uuid import UUID
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.repositories import DataRepository
from src.features.blogs.domain.entities import Blog
from src.features.blogs.domain.schemas import BlogPublic

class DeleteBlog:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self, 
        user_id: UUID,
        blog_id: UUID
    ):
        blog: Blog = self.__repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise NotFoundException("Blog not found")
        
        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_blog = self.__repository.delete(
            key="blog_id",
            value=blog.blog_id
        )

        return BlogPublic.model_validate(deleted_blog, from_attributes=True)
