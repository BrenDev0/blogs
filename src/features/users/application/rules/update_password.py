from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.security.domain.services.hashing import HashingService
from src.features.users.domain.entities import User
from src.security.domain.exceptions import IncorrectPassword

class UpdatePasswordRule:
    def __init__(
        self,
        repository: data_repository.DataRepository,
        hashing: HashingService
    ):
        self.__repository = repository
        self.__hashing = hashing


    def validate(
        self,
        user_id: UUID,
        new_password: str,
        old_password: str = None,
        current_password_check: bool = True
    ):
        user: User = self.__repository.get_one(
            key="user_id",
            value=user_id
        )

        if not user:
            raise exceptions.NotFoundException("User not found")
        
        # check new and old password match
        is_current_password = self.__hashing.compare_password(
            password=new_password,
            hashed_password=user.password,
            throw_error=False
        )

        if is_current_password:
            raise IncorrectPassword("New password cannot be same as current password")
        
        if current_password_check:
            if not old_password:
                raise ValueError("Old password required for check")
        
            self.__hashing.compare_password(
                password=old_password,
                hashed_password=user.password,
                detail="Incorrect password",
                throw_error=True
            )
            
        return True
        
        