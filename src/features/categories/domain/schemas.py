from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime

class CategoryBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        extra="forbid",
        alias_generator=to_camel,
        str_min_length=1
    )

class CategoryPublic(CategoryBase):
    category_id: UUID
    user_id: UUID
    name: str
    created_at: datetime

class CreateCategoryRequest(CategoryBase):
    name: str

class UpdateCategoryRequest(CategoryBase):
    name: str

