import strawberry
from src.features.comments.domain.schemas import CommentPublic


@strawberry.experimental.pydantic.type(model=CommentPublic, all_fields=True)
class CommentType:
    pass