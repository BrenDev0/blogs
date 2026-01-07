from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.blogs.domain import schemas, entities

class GetBlogResource:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository


    def execute(
        self,
        user_id: UUID,
        blog_id: UUID
    ):
        blog: entities.Blog = self.__repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise exceptions.NotFoundException("Blog not found")

        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        return schemas.BlogPublic.model_validate(blog, from_attributes=True)