import strawberry
from src.features.posts.domain.schemas import BlogPostPublic

@strawberry.experimental.pydantic.type(BlogPostPublic, all_fields=True)
class BlogPostType: 
    pass