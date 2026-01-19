from functools import wraps
from strawberry.types import Info
from src.security.dependencies.services import get_web_token_service
from src.security.domain.exceptions import ExpiredToken, InvalidToken
from src.app.domain.exceptions import GraphQlException


def inject_strawberry_context(resolver):
    @wraps(resolver)
    def wrapper(*args, **kwargs):
        # Find Info object (Strawberry passes it as kwarg or positional)
        info: Info | None = kwargs.get("info")

        if info is None:
            for arg in args:
                if isinstance(arg, Info):
                    info = arg
                    break

        if info is None:
            return resolver(*args, **kwargs)

        request = info.context.get("request")
        if not request:
            return resolver(*args, **kwargs)

        authorization = request.headers.get("authorization")

        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "", 1)
            web_token_service = get_web_token_service()

            try:
                payload = web_token_service.decode(token)

                for key, value in payload.items():
                    info.context[key] = value

            except (ExpiredToken, InvalidToken) as e:
                raise GraphQlException(str(e))
            
            except Exception:
                raise GraphQlException()

        return resolver(*args, **kwargs)

    return wrapper
