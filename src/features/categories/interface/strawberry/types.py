import strawberry
from src.features.categories.domain.schemas import CategoryPublic

@strawberry.experimental.pydantic.type(CategoryPublic, all_fields=True)
class CategoryType:
    pass