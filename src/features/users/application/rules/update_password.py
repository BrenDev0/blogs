from uuid import UUID
from src.persistence.domain.repositories import DataRepository
from src.security.domain.services.hashing import HashingService
from src.features.users.domain.entities import User
from src.persistence.domain.exceptions import NotFoundException


class UpdatePasswordRule:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService
    ):
        self.__repository = repository
        self.__hashing = hashing


    def validate(
        self,
        user_id: UUID,
        old_password: str
    ):
        user: User = self.__repository.get_one(
            key="user_id",
            value=user_id
        )

        if not user:
            raise NotFoundException("User not found")
        
        self.__hashing.compare_password(
            password=old_password,
            hashed_password=user.password,
            detail="Incorrect password",
            throw_error=True
        )
        
        