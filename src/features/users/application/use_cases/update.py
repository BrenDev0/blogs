from uuid import UUID
from src.features.users.domain.schemas import UpdateUserSchema, UserPublic
from src.features.users.domain.entities import User
from src.security.domain.services.encryption import EncryptionService
from src.security.domain.services.hashing import HashingService
from src.persistence.domain.repositories import DataRepository
from src.persistence.domain.exceptions import NotFoundException

class UpdateUser:
    def __init__(
        self, 
        repository: DataRepository,
        encryption: EncryptionService,
        hashing: HashingService
    ):
        self.__repository = repository
        self.__encryption = encryption
        self.__hashing = hashing

    def execute(self, user_id: UUID, changes: UpdateUserSchema) -> UserPublic:
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
        
        updated_user: User = self.__repository.update(
            key="user_id",
            value=user_id,
            changes=processed_changes
        )

        if not updated_user:
            raise NotFoundException("User not found")
        
        
        return UserPublic(
            user_id=updated_user.user_id,
            email=self.__encryption.decrypt(updated_user.email),
            name=self.__encryption.decrypt(updated_user.name),
            created_at=updated_user.created_at
        )