from uuid import UUID 
from src.persistence.domain.data_repository import DataRepository
from src.features.categories.domain.schemas import CategoryPublic

class GetCategoryCollection:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        user_id: UUID
    ):
        categories = self.__repository.get_many(
            key="user_id",
            value=user_id
        )

        return [
            CategoryPublic.model_validate(category, from_attributes=True) for category in categories
        ] if categories else []
    


        
