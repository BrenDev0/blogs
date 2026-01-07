from uuid import UUID
from src.security.domain.services.encryption import EncryptionService
from src.features.users.domain import schemas, entities
from src.persistence.domain import data_repository, exceptions

class DeleteUser:
    def __init__(
       self,
        repository: data_repository.DataRepository,
        encryption: EncryptionService
    ) -> schemas.UserPublic:
        self.__repository = repository
        self.__encryption = encryption


    def execute(
        self,
        user_id: UUID
    ):
        deleted_user: entities.User =  self.__repository.delete(
            key="user_id",
            value=user_id
        )

        if not deleted_user:
            raise exceptions.NotFoundException("User not found")

        return schemas.UserPublic(
            user_id=deleted_user.user_id,
            email=self.__encryption.decrypt(deleted_user.email),
            name=self.__encryption.decrypt(deleted_user.name),
            created_at=deleted_user.created_at
        ) 