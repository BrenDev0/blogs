import typing
from strawberry.permission import BasePermission
from strawberry.types import Info
from src.security.dependencies.services import get_web_token_service
from src.security.domain.exceptions import ExpiredToken, InvalidToken
from src.app.domain.exceptions import GraphQlException

class UserAuth(BasePermission):
     message = "Unauthorized"
     def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request = info.context["request"]
       
        authorization = request.headers.get("authorization") 
        
        if authorization:
            web_token_service = get_web_token_service()
            token = authorization.split("Bearer ")[-1]
            try:
                payload = web_token_service.decode(token)
                user_id = payload.get("user_id")
                if user_id:
                    info.context["user_id"] = user_id
                    return True
            
            except ExpiredToken as e:
                self.message = str(e)

            except InvalidToken as e:
                self.message = str(e)

            except Exception:
                raise GraphQlException()
            
        raise GraphQlException(self.message)