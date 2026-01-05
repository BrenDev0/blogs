import strawberry
from src.features.blogs.domain.schemas import BlogPublic

@strawberry.experimental.pydantic.type(model=BlogPublic, all_fields=True)
class BlogType:
    pass