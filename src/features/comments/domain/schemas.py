from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime

class CommentConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        str_min_length=1,
        alias_generator=to_camel
    )

class CommentPublic(CommentConfig):
    comment_id: UUID
    post_id: UUID
    text: str
    approved: bool
    created_at: datetime

class CreateCommentRequest(CommentConfig):
    text: str

