from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime

class ImageConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel
    )

class ImagePublic(ImageConfig):
    image_id: UUID
    post_id: UUID
    url: str
    uploaded_at: datetime
