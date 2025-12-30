from src.persistence.domain.repositories import DataRepository
from src.security.domain.services.hashing import HashingService
from src.security.domain.services.encryption import EncryptionService
from src.users.domain.schemas import UserPublic
from src.users.domain.entities import User

class CreateUser:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService,
        encryption: EncryptionService
    ):
        self.__repository = repository
        self.__hashing = hashing
        self.__encrytpion = encryption

    
    def execute(
        self,
        name: str,
        email: str,
        password: str
    ):
        hashed_password = self.__hashing.hash_password(password=password)
        hashed_email = self.__hashing.hash_for_search(data=email)

        encrypted_name = self.__encrytpion.encrypt(name)
        encrypted_email = self.__encrytpion.encrypt(email)

        user = User(
            name=encrypted_name,
            email=encrypted_email,
            password=hashed_password,
            email_hash=hashed_email
        )

        new_user: User = self.__repository.create(data=user)

        user_public = UserPublic(
            user_id=new_user.user_id,
            email=self.__encrytpion.decrypt(new_user.email),
            name=self.__encrytpion.decrypt(new_user.name),
            created_at=new_user.created_at
        )

        return user_public