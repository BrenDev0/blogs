from uuid import UUID
from src.persistence.domain import exceptions, data_repository
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain import entities, schemas
from src.features.blogs.domain.entities import Blog

class CreateCategory:
    def __init__(
        self,
        category_repository: data_repository.DataRepository,
        blogs_repository: data_repository.DataRepository
    ):
        self.__category_repository = category_repository
        self.__blogs_repository = blogs_repository
    

    
    def execute(
        self,
        blog_id: UUID,
        user_id: UUID,
        req_data: schemas.CreateCategoryRequest
    ):
        blog: Blog = self.__blogs_repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise exceptions.NotFoundException("Blog not found")
        
        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        data = entities.Category(
            **req_data.model_dump(),
            blog_id=blog_id
        )

        new_category = self.__category_repository.create(
            data=data
        )

        return schemas.CategoryPublic.model_validate(new_category, from_attributes=True)