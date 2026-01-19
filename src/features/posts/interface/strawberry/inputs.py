import strawberry
from typing import Optional
from uuid import UUID
from src.features.posts.domain.schemas import CreateBlogPostRequest, UpdateBlogPostRequest

@strawberry.experimental.pydantic.input(CreateBlogPostRequest, all_fields=True)
class CreateBlogPostInput:
    pass

@strawberry.input()
class UpdateBlogPostInput:
    category_id: Optional[UUID] = strawberry.UNSET
    author: Optional[str] = strawberry.UNSET
    title: Optional[str] = strawberry.UNSET
    content_1: Optional[str] = strawberry.UNSET
    content_2: Optional[str] = strawberry.UNSET
    published: Optional[bool] = strawberry.UNSET
    allow_comments: Optional[bool] = strawberry.UNSET