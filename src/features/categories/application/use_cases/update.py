from uuid import UUID 
from src.persistence.domain import repositories, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain import entities, schemas


class UpdateCategory:
    def __init__(
        self,
        repository: repositories.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        category_id: UUID,
        changes: schemas.UpdateCategoryRequest
    ):
        category: entities.Category = self.__repository.get_one(
            key="category_id",
            value=category_id
        )

        if not category:
            raise exceptions.NotFoundException("Category not found")
        
        if str(category.user_id) != str(user_id):
            raise PermissionsException()
        
        updated_category = self.__repository.update(
            key="category_id",
            value=category.category_id,
            changes=changes.model_dump(exclude_none=True)
        )

        return schemas.CategoryPublic.model_validate(updated_category, from_attributes=True)