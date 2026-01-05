from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from typing import Optional
from datetime import datetime

class BlogBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        extra="forbid",
        str_min_length=1,
        alias_generator=to_camel
    )

class BlogPublic(BlogBase):
    blog_id: UUID
    user_id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

class CreateBlogRequest(BlogBase):
    name: str
    description: Optional[str] = None

class UpdateBlogRequest(BlogBase):
    name: Optional[str] = None
    description: Optional[str] = None

