import strawberry
from src.features.posts.domain.schemas import CreateBlogPostRequest, UpdateBlogPostRequest

@strawberry.experimental.pydantic.input(CreateBlogPostRequest, all_fields=True)
class CreateBlogPostInput:
    pass

@strawberry.experimental.pydantic.input(UpdateBlogPostRequest, all_fields=True)
class UpdateBlogPostInput:
    pass