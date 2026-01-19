import strawberry
from src.features.email.domain.schemas import VerifyEmail

@strawberry.experimental.pydantic.input(model=VerifyEmail, all_fields=True)
class VerifyEmailType:
    pass

@strawberry.type
class VerificationTokenType:
    verification_token: str

@strawberry.type
class EmailConfirmationType:
    message: str