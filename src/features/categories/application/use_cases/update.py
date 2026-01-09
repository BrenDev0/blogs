from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain import entities, schemas


class UpdateCategory:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        category_id: UUID,
        changes: schemas.UpdateCategoryRequest
    ):
        cleaned_changes = changes.model_dump(exclude_none=True, by_alias=False)
        if not cleaned_changes:
            raise exceptions.UpdateFieldsException()
        
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
            changes=cleaned_changes
        )

        return schemas.CategoryPublic.model_validate(updated_category, from_attributes=True)