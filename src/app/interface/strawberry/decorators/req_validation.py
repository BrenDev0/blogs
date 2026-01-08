from functools import wraps
from pydantic import ValidationError
from src.app.domain.exceptions import GraphQlException

def validate_input_to_model(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        input_arg = kwargs.get("input")
        if input_arg is not None:
            try:
                kwargs["input"] = input_arg.to_pydantic()
                
            except ValidationError as e:
                raise GraphQlException(str(e))
        return fn(*args, **kwargs)
    return wrapper