import logging
import strawberry
from src.features.users.dependencies.use_cases import get_user_use_case
from src.features.users.interface.strawberry.types import UserType
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.middleware.user_auth import UserAuth
logger = logging.getLogger(__name__)

@strawberry.type
class UserQueries:
    @strawberry.field(
        permission_classes=[UserAuth],
        description="Get User from id in Auth token"
    )
    def get_me(
        self,
        info: strawberry.Info
    ) -> UserType | None:
        use_case = get_user_use_case()

        try:
            user_id = info.context.get("user_id")
            
            return use_case.execute(
                key="user_id",
                value=user_id
            )

        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()