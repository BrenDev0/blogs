from src.persistence.domain import repositories, exceptions
from src.security.domain.services import hashing, encryption
from src.features.users.domain import schemas, entities
from datetime import datetime, timezone

class UserLogin:
    def __init__(
        self,
        repository: repositories.DataRepository,
        hashing: hashing.HashingService,
        encryption: encryption.EncryptionService
    ) -> schemas.UserPublic:
        self.__repository = repository
        self.__hashing = hashing
        self.__encrytpion = encryption

    
    def execute(
        self,
        email: str,
        password: str
    ):
        
        hashed_email = self.__hashing.hash_for_search(email)

        user_exists: entities.User = self.__repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if not user_exists:
            raise exceptions.NotFoundException("User not found")

        self.__hashing.compare_password(
            password=password,
            hashed_password=user_exists.password,
            detail="Incorrect email or password",
            throw_error=True
        )

        user_public = schemas.UserPublic(
            user_id=user_exists.user_id,
            email=self.__encrytpion.decrypt(user_exists.email),
            name=self.__encrytpion.decrypt(user_exists.name),
            created_at=user_exists.created_at
        )

        return user_public