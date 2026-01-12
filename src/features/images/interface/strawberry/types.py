import strawberry
from typing import List
from src.features.images.domain.schemas import ImagePublic

@strawberry.experimental.pydantic.type(model=ImagePublic, all_fields=True)
class ImageType:
    pass


@strawberry.type
class UploadType:
    success: List[ImageType]
    failed: List[str]