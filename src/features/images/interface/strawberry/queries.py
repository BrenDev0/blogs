import strawberry
from uuid import UUID
from src.features.images.interface.strawberry import types

@strawberry.type
class ImageQueries:
    @strawberry.field
    def image_collection(
        self,
        post_id: UUID,
        info: strawberry.Info
    ) -> types.ImageType:
        pass