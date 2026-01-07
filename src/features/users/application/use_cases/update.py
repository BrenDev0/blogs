from uuid import UUID
from src.features.users.domain import schemas, entities
from src.security.domain.services import encryption, hashing
from src.persistence.domain import repositories, exceptions

class UpdateUser:
    def __init__(
        self, 
        repository: repositories.DataRepository,
        encryption: encryption.EncryptionService,
        hashing: hashing.HashingService
    ):
        self.__repository = repository
        self.__encryption = encryption
        self.__hashing = hashing

    def execute(
        self, 
        user_id: UUID, 
        changes: schemas.UpdateUserSchema
    ) -> schemas.UserPublic:
        cleaned_changes = changes.model_dump(exclude_unset=True)
        
        processed_changes = {}
        
        for key, value in cleaned_changes.items():
            if key == "name":
                processed_changes["name"] = self.__encryption.encrypt(value)
            elif key == "email":
                processed_changes["email"] = self.__encryption.encrypt(value)
                processed_changes["email_hash"] = self.__hashing.hash_for_search(value)
            elif key == "password":
                processed_changes["password"] = self.__hashing.hash_password(value)
            else:
                processed_changes[key] = value
        
        updated_user: entities.User = self.__repository.update(
            key="user_id",
            value=user_id,
            changes=processed_changes
        )

        if not updated_user:
            raise exceptions.NotFoundException("User not found")
        
        
        return schemas.UserPublic(
            user_id=updated_user.user_id,
            email=self.__encryption.decrypt(updated_user.email),
            name=self.__encryption.decrypt(updated_user.name),
            created_at=updated_user.created_at
        )