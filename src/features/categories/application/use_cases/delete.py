from uuid import UUID 
from src.persistence.domain import data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.categories.domain import entities, schemas

class DeleteCategory:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        category_id: UUID
    ):
        category: entities.Category = self.__repository.get_one(
            key="category_id",
            value=category_id
        ) 

        if not category:
            raise exceptions.NotFoundException("Category not found")
        
        if str(category.user_id) != str(user_id):
            raise PermissionsException()
        
        deleted_category = self.__repository.delete(
            key="category_id",
            value=category.category_id
        )
        return schemas.CategoryPublic.model_validate(deleted_category, from_attributes=True)
