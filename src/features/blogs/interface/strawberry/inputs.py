import strawberry
from src.features.blogs.domain.schemas import CreateBlogRequest, UpdateBlogRequest

@strawberry.experimental.pydantic.input(CreateBlogRequest, all_fields=True)
class CreateBlogInput:
    pass

@strawberry.experimental.pydantic.input(UpdateBlogRequest, all_fields=True)
class UpdateBlogInput:
    pass