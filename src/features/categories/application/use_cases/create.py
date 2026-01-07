from uuid import UUID
from src.persistence.domain.repositories import DataRepository
from src.features.categories.domain import entities, schemas

class CreateCategory:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        req_data: schemas.CreateCategoryRequest
    ):
        data = entities.Category(
            **req_data.model_dump(),
            user_id=user_id
        )

        new_category = self.__repository.create(
            data=data
        )

        return schemas.CategoryPublic.model_validate(new_category, from_attributes=True)