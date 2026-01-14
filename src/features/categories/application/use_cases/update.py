from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain import entities, schemas
from src.features.blogs.domain.entities import Blog

class UpdateCategory:
    def __init__(
        self,
        category_repository: data_repository.DataRepository,
        blog_repository: data_repository.DataRepository
    ):
        self.__category_repository = category_repository
        self.__blog_repository = blog_repository

    def execute(
        self,
        user_id: UUID,
        category_id: UUID,
        changes: schemas.UpdateCategoryRequest
    ):
        cleaned_changes = changes.model_dump(exclude_none=True, by_alias=False)
        if not cleaned_changes:
            raise exceptions.UpdateFieldsException()

        
        category: entities.Category = self.__category_repository.get_one(
            key="category_id",
            value=category_id
        )

        if not category:
            raise exceptions.NotFoundException("Category not found")
        
        blog: Blog = self.__blog_repository.get_one(
            key="blog_id",
            value=category.blog_id
        )
        
        if not blog:
            self.__category_repository.delete(
                key="category_id",
                value=category.category_id
            )

            raise exceptions.NotFoundException("Category not availbale")
        

        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_category = self.__category_repository.update(
            key="category_id",
            value=category.category_id,
            changes=cleaned_changes
        )

        return schemas.CategoryPublic.model_validate(updated_category, from_attributes=True)