from typing import Any
from uuid import UUID

class TypeValidationService:
    def __init__(self):
        self._available_validations = {
            "int": self.validate_int,
            "uuid": self.validate_uuid,
            "bool": self.validate_bool
        }

    def validate(
       self,
       expected_type: str,
       value_to_check: Any     
    ):
        if expected_type not in self._available_validations:  
            raise ValueError(
                f"{expected_type} not available, current validations: {', '.join(self._available_validations.keys())}"  
            )

        return self._available_validations[expected_type.lower()](value_to_check)  

    def validate_bool(
        self,
        value_to_check: Any
    ):
        if isinstance(value_to_check, bool):  
            return value_to_check
            
        if isinstance(value_to_check, str):
            lower = value_to_check.lower()
            if lower in ("true", "1", "yes"):
                return True
            elif lower in ("false", "0", "no"):
                return False
            else:
                raise ValueError(
                    f"Expected boolean (true/false), got '{value_to_check}'"  
                )
        elif isinstance(value_to_check, (int, float)):
            return bool(value_to_check)
        raise ValueError(
            f"Expected boolean, got {type(value_to_check).__name__}"  
        )
    
    def validate_int(
        self, 
        value_to_check: Any
    ):
        if isinstance(value_to_check, int):
            return value_to_check
            
        try:
            return int(value_to_check)
        except (ValueError, TypeError):
            raise ValueError(
                f"Expected integer, got '{value_to_check}'" 
            )
        
    def validate_uuid(
        self,
        value_to_check: Any
    ):
        if isinstance(value_to_check, UUID):  
            return value_to_check
            
        try:
            return UUID(str(value_to_check))
        except (ValueError, TypeError):
            raise ValueError(
                f"Expected UUID, got '{value_to_check}'"  
            )