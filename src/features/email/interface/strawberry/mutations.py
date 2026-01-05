import logging
import strawberry
from src.features.email.interface.strawberry.types import VerificationTokenType, VerifyEmailType
from src.features.email.dependencies.use_cases import get_verification_email_use_case
from src.features.users.dependencies.business_rules import get_unique_email_rule
from src.security.dependencies.services import get_web_token_service
from src.features.users.domain.exceptions import EmailInUseException
from src.security.utils.random_code_generator import get_random_code
from src.app.domain.exceptions import GraphQlException
logger = logging.getLogger(__name__)


@strawberry.type
class EmailMutations:
    @strawberry.mutation(
        description="Send verification code to users email. Will receive a token that can be used for verified requests."
    )
    def verify_email(
        self,
        input: VerifyEmailType
    ) -> VerificationTokenType:
        use_case = get_verification_email_use_case()
        rule = get_unique_email_rule()
        try: 
            rule.validate(
                email=input.email
            )

            code = get_random_code(len=6)

            use_case.execute(
                to=input.email,
                verification_code=code
            )

            web_token_service = get_web_token_service()
            token_payload = {
                "verification_code": code
            }
            verification_token = web_token_service.generate(payload=token_payload, expiration=900) # 15 mins

            return VerificationTokenType(
                verification_token=verification_token
            )


        except EmailInUseException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()