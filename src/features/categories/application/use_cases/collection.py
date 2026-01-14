from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.features.categories.domain.schemas import CategoryPublic
from src.features.blogs.domain.entities import Blog


class GetCategoryCollection:
    def __init__(
        self,
        category_repository: data_repository.DataRepository,
        blog_repository: data_repository.DataRepository
    ):
        self.__category_repository = category_repository
        self.__blog_repository = blog_repository

    
    def execute(
        self,
        blog_id: UUID
    ):
        blog: Blog = self.__blog_repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise exceptions.NotFoundException("Blog not found")

        categories = self.__category_repository.get_many(
            key="blog_id",
            value=blog.blog_id
        )

        return [
            CategoryPublic.model_validate(category, from_attributes=True) for category in categories
        ] if categories else []
    


        
