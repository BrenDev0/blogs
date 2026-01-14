import strawberry
from src.features.comments.domain.schemas import CreateCommentRequest

@strawberry.experimental.pydantic.input(model=CreateCommentRequest, all_fields=True)
class CreateCommentInput:
    pass

