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
                messages = str(e).split('For further information visit https://errors.pydantic.dev/2.12/v/string_too_short')
                cleaned_messages = [
                    message.replace("[type=string_too_short, input_value='', input_type=str]", "") for  message in messages
                ]
                raise GraphQlException(f"{" ".join(cleaned_messages).strip()}")
        return fn(*args, **kwargs)
    return wrapper