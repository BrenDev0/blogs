from src.persistence.domain.repositories import DataRepository
from src.security.domain.services.encryption import EncryptionService
from src.features.users.domain.schemas import UserPublic
from src.features.users.domain.entities import User

class GetUser:
    def __init__(
        self,
        repository: DataRepository,
        encryption: EncryptionService
    ):
        self.__repository = repository
        self.__encryption = encryption

    def execute(
        self,
        key: str,
        value: str
    ) -> UserPublic | None:
        user: User = self.__repository.get_one(
            key=key,
            value=value
        )

        if user:
            return UserPublic(
                user_id=user.user_id,
                email=self.__encryption.decrypt(user.email),
                name=self.__encryption.decrypt(user.name),
                created_at=user.created_at
            )

        return None
    
