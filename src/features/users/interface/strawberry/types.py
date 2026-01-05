import strawberry
from src.features.users.domain.schemas import UserPublic

@strawberry.experimental.pydantic.type(model=UserPublic, all_fields=True)
class UserType:
    pass

@strawberry.type
class UserWithTokenType:
    user: UserType
    token: str