from uuid import UUID
from src.features.users.domain.entities import User
from src.security.domain.exceptions import PermissionsException
from src.persistence.domain.repositories import DataRepository

class IsAdmin:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    
    def check(
        self,
        user_id: UUID
    ):
        user: User = self.__repository.get_one(
            key="user_id",
            value=user_id
        )

        if not user.is_admin:
            raise PermissionsException("Forbidden")