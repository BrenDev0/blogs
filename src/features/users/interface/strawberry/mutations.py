import logging
import strawberry
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.interface.strawberry.middleware import user_auth, user_verification
from src.app.domain.exceptions import GraphQlException
from src.persistence.domain.exceptions import NotFoundException, UpdateFieldsException
from src.security.domain.exceptions import IncorrectPassword
from src.features.users.interface.strawberry import inputs, types
from src.features.users.domain.schemas import UpdateUserSchema

from src.features.users.dependencies.use_cases import (
    get_create_user_use_case, 
    get_login_use_case, 
    get_delete_user_use_case, 
    get_update_user_use_case
)
from src.features.users.dependencies.business_rules import get_update_password_rule
from src.security.dependencies.services import get_web_token_service
logger = logging.getLogger(__name__)

@strawberry.type
class UserMutations:
    @strawberry.mutation(
        permission_classes=[user_verification.UserVerification],
        description="Verification token from verify email must be used as Auth Bearer."
    )
    @validate_input_to_model
    def create_user(
        self,
        info: strawberry.Info,
        input: inputs.CreateUserInput
    ) -> types.UserWithTokenType:
        verification_code = info.context.get("verification_code")
        if int(input.code) != int(verification_code):
            raise GraphQlException("Unauthorized")
        
        try:
            use_case = get_create_user_use_case()
            web_token_service = get_web_token_service()
            
            new_user = use_case.execute(
                req_data=input
            )

            token_payload = {
                "user_id": str(new_user.user_id)
            }

            token = web_token_service.generate(
                payload=token_payload,
                expiration=604800 # 7 days
            )

            return types.UserWithTokenType(
                user=new_user,
                token=token
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
    
    @strawberry.mutation(
        permission_classes=[user_auth.UserAuth],
        description="Update user by user id in auth token"
    )
    @validate_input_to_model
    def update_user(
        self,
        info: strawberry.Info,
        input: inputs.UpdateUserInput
    ) -> types.UserType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_update_user_use_case()

            changes = {}
            if input.old_password:
                if not input.password:
                    raise GraphQlException("New password requiered to update password")
                
            if input.password:
                if not input.old_password:
                    raise GraphQlException("Old password requiered to update password")
            
                rule = get_update_password_rule()
                rule.validate(
                    user_id=user_id,
                    old_password=input.old_password,
                    new_password=input.password,
                    current_password_check=True
                )

                changes["password"] = input.password

            if input.name is not None:
                changes["name"] = input.name

            return use_case.execute(
                user_id=user_id,
                changes=UpdateUserSchema(**changes)
            )
            
        except (NotFoundException, IncorrectPassword, UpdateFieldsException) as e:
            raise GraphQlException(str(e))
            
        except GraphQlException:
            raise

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        description="Update email, or password for account recovery",
        permission_classes=[user_verification.UserVerification]
    )
    @validate_input_to_model
    def verified_update(
        self,
        info: strawberry.Info,
        input: inputs.VerifiedUserUpdateInput
    ) -> types.UserType:
        user_id = info.context.get("user_id")
        if not user_id:
            raise GraphQlException("Forbidden")
            
        verification_code = info.context.get("verification_code")
        if int(input.code) != int(verification_code):
            raise GraphQlException("Unauthorized")
        
        if input.email and input.password:
            raise GraphQlException("Cannot update email and password simultaneously")
        
        try:    
            use_case = get_update_user_use_case()
            if input.password:
                rule = get_update_password_rule()

                rule.validate(
                    user_id=user_id,
                    new_password=input.password,
                    current_password_check=False
                )

            changes = UpdateUserSchema(
                **input.model_dump(exclude_none=True, exclude={"code"})
            )

            return use_case.execute(
                user_id=user_id,
                changes=changes
            )
        
        except (NotFoundException, IncorrectPassword, UpdateFieldsException) as e:
            raise GraphQlException(str(e))

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    
    # @strawberry.mutation(
    #     description="Update users password for account recovery",
    #     permission_classes=[user_auth.UserAuth]
    # )
    # def account_recovery_update_password(
    #     self,
    #     info: strawberry.Info,
    #     input: inputs.VerifiedUserUpdateInput
    # ) -> types.UserWithTokenType:
    #     pass

    @strawberry.mutation(
        description="User login"
    )
    @validate_input_to_model
    def login(
        self,
        input: inputs.LoginInput
    ) -> types.UserWithTokenType:
        try:
            use_case = get_login_use_case()
            web_token_service = get_web_token_service()

            user = use_case.execute(
                email=input.email,
                password=input.password
            )
            token_payload = {
                "user_id": str(user.user_id)
            }

            token = web_token_service.generate(
                payload=token_payload,
                expiration=604800 # 7 days
            )

            return types.UserWithTokenType(
                user=user,
                token=token
            )
        
        except (NotFoundException, IncorrectPassword):
            raise GraphQlException("Incorrect email or password")

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        

    @strawberry.mutation(
        permission_classes=[user_auth.UserAuth],
        description="Delete user by id in auth token"
    )
    def delete_user(
        self,
        info: strawberry.Info
    ) -> types.UserType:
        try:
            user_id = info.context.get("user_id")
            use_case = get_delete_user_use_case()

            return use_case.execute(
                user_id=user_id
            )

        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    

