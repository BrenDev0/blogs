import logging
import strawberry
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.decorators import req_validation, gather_context
from src.persistence.domain.exceptions import NotFoundException
from src.security.dependencies.services import get_web_token_service, get_encrytpion_service
from src.security.utils.random_code_generator import get_random_code
from src.features.email.interface.strawberry.types import VerificationTokenType, VerifyEmailType
from src.features.email.dependencies.use_cases import get_verification_email_use_case
from src.features.users.dependencies.business_rules import get_unique_email_rule, get_user_exists_rule
from src.features.users.domain.exceptions import EmailInUseException
logger = logging.getLogger(__name__)


@strawberry.type
class EmailMutations:
    @strawberry.mutation(
        description="Send verification code to users email. Will receive a token that can be used for verified requests. This endpoint can also be used with an Auth header to recieve token needed for verifed update to users email"
    )
    @req_validation.validate_input_to_model
    @gather_context.inject_strawberry_context
    def verify_email(
        self,
        info: strawberry.Info,
        input: VerifyEmailType
    ) -> VerificationTokenType:
        try: 
            use_case = get_verification_email_use_case()
            rule = get_unique_email_rule()
            
            rule.validate(
                email=input.email
            )

            code = get_random_code(len=6)

            use_case.execute(
                to=input.email,
                verification_code=code
            )

            web_token_service = get_web_token_service()
            encryption = get_encrytpion_service()

            token_payload = {
                "verification_code": encryption.encrypt(code)
            }

            user_id = info.context.get("user_id")

            if user_id:
                token_payload["user_id"] = user_id

            verification_token = web_token_service.generate(payload=token_payload, expiration=900) # 15 mins

            return VerificationTokenType(
                verification_token=verification_token
            )


        except EmailInUseException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    @strawberry.mutation(
        description="Searches for user in db and sends email verification email, token recieved must be used for verified update to users password"
    )
    @req_validation.validate_input_to_model
    def public_account_recovery(
        self,
        input: VerifyEmailType
    ) -> VerificationTokenType:
        try:
            use_case = get_verification_email_use_case()
            rule = get_user_exists_rule()
        
            existing_user = rule.validate(email=input.email)

            code = get_random_code(len=6)

            use_case.execute(to=input.email, verification_code=code)

            web_token_service = get_web_token_service()
            encryption = get_encrytpion_service()

            token_payload = {
                "user_id": str(existing_user.user_id),
                "verification_code": encryption.encrypt(code)
            }

            verification_token = web_token_service.generate(
                payload=token_payload,
                expiration=900
            )

            return VerificationTokenType(
                verification_token=verification_token
            )
        
        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()





            
        
    