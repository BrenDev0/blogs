from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from typing import Optional
from datetime import datetime

class BlogPostConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        extra="ignore",
        str_min_length=1
    )

class BlogPostPublic(BlogPostConfig):
    post_id: Optional[UUID] = None
    blog_id: UUID
    category_id: Optional[UUID] = None
    author: str
    title: str
    content_1: str
    content_2: Optional[str] = None
    published: Optional[bool] = False
    published_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

class CreateBlogPostRequest(BlogPostConfig):
    category_id: Optional[UUID] = None
    author: str
    title: str
    content_1: str
    content_2: Optional[str] = None
    published: Optional[bool] = False

class UpdateBlogPostRequest(BlogPostConfig):
    category_id: Optional[UUID] = None
    author: Optional[UUID] = None
    title: Optional[str] = None
    content_1: Optional[str] = None
    content_2: Optional[str] = None
    published: Optional[bool] = None