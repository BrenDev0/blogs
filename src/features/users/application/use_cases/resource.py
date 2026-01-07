from src.persistence.domain.data_repository import DataRepository
from src.security.domain.services.encryption import EncryptionService
from src.features.users.domain import schemas, entities

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
    ) -> schemas.UserPublic | None:
        user: entities.User = self.__repository.get_one(
            key=key,
            value=value
        )

        if user:
            return schemas.UserPublic(
                user_id=user.user_id,
                email=self.__encryption.decrypt(user.email),
                name=self.__encryption.decrypt(user.name),
                created_at=user.created_at
            )

        return None
    
