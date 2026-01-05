from uuid import UUID 
from src.persistence.domain.repositories import DataRepository
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain.entities import Category
from src.features.categories.domain.schemas import CategoryPublic, UpdateCategoryRequest


class UpdateCategory:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        category_id: UUID,
        changes: UpdateCategoryRequest
    ):
        category: Category = self.__repository.get_one(
            key="category_id",
            value=category_id
        )

        if not category:
            raise NotFoundException("Category not found")
        
        if str(category.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_category = self.__repository.update(
            key="category_id",
            value=category.category_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return CategoryPublic.model_validate(updated_category, from_attributes=True)