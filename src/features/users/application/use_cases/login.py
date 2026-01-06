from src.persistence.domain.repositories import DataRepository
from src.security.domain.services.hashing import HashingService
from src.security.domain.services.encryption import EncryptionService
from src.features.users.domain.schemas import UserPublic
from src.persistence.domain.exceptions import NotFoundException
from src.features.users.domain.entities import User
from datetime import datetime, timezone

class UserLogin:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService,
        encryption: EncryptionService
    ) -> UserPublic:
        self.__repository = repository
        self.__hashing = hashing
        self.__encrytpion = encryption

    
    def execute(
        self,
        email: str,
        password: str
    ):
        
        hashed_email = self.__hashing.hash_for_search(email)

        user_exists: User = self.__repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if not user_exists:
            raise NotFoundException("User not found")

        self.__hashing.compare_password(
            password=password,
            hashed_password=user_exists.password,
            detail="Incorrect email or password",
            throw_error=True
        )

        user_public = UserPublic(
            user_id=user_exists.user_id,
            email=self.__encrytpion.decrypt(user_exists.email),
            name=self.__encrytpion.decrypt(user_exists.name),
            created_at=user_exists.created_at
        )

        return user_public