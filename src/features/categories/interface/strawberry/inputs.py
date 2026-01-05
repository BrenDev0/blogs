import strawberry
from src.features.categories.domain.schemas import (
    CreateCategoryRequest,
    UpdateCategoryRequest
)

@strawberry.experimental.pydantic.input(CreateCategoryRequest, all_fields=True)
class CreateCategoryInput:
    pass

@strawberry.experimental.pydantic.input(UpdateCategoryRequest, all_fields=True)
class UpdateCategoryInput:
    pass