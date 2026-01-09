import strawberry
from src.features.images.domain.schemas import ImagePublic

@strawberry.experimental.pydantic.type(model=ImagePublic, all_fields=True)
class imageType:
    pass