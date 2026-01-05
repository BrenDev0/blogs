from uuid import UUID
from src.persistence.domain.repositories import DataRepository
from src.features.categories.domain.entities import Category
from src.features.categories.domain.schemas import CategoryPublic, CreateCategoryRequest

class CreateCategory:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID,
        req_data: CreateCategoryRequest
    ):
        data = Category(
            **req_data.model_dump(),
            user_id=user_id
        )

        new_category = self.__repository.create(
            data=data
        )

        return CategoryPublic.model_validate(new_category, from_attributes=True)