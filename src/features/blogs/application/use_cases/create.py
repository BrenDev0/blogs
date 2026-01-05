from uuid import UUID
from src.features.blogs.domain.schemas import CreateBlogRequest, BlogPublic
from src.persistence.domain.repositories import DataRepository
from src.features.blogs.domain.entities import Blog

class CreateBlog:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        req_data: CreateBlogRequest
    ):
        blog_data = Blog(
            **req_data.model_dump(exclude_none=True),
            user_id=user_id
        )

        new_blog: Blog = self.__repository.create(
            data=blog_data
        )

        return BlogPublic.model_validate(new_blog, from_attributes=True)