from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.features.blogs.domain.schemas import BlogPublic

class GetBlogsCollection:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID
    ):
        blogs = self.__repository.get_many(
            key="user_id",
            value=user_id
        )

        return [
            BlogPublic.model_validate(blog, from_attributes=True) for blog in blogs
        ] if blogs else []