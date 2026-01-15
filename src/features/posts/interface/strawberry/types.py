import strawberry
from typing import List
from src.features.posts.domain.schemas import BlogPostPublic
from src.features.images.interface.strawberry.types import ImageType


@strawberry.experimental.pydantic.type(BlogPostPublic, all_fields=True)
class BlogPostType: 
    pass

@strawberry
class BlogPostWithUploadType:
    post: BlogPostType
    images: List[ImageType]
    failed_uploads: List[str]