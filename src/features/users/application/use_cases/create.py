from src.persistence.domain.repositories import DataRepository
from src.security.domain.services import hashing, encryption
from src.features.users.domain import schemas, entities

class CreateUser:
    def __init__(
        self,
        repository: DataRepository,
        hashing: hashing.HashingService,
        encryption: encryption.EncryptionService
    ):
        self.__repository = repository
        self.__hashing = hashing
        self.__encrytpion = encryption

    
    def execute(
        self,
        req_data: schemas.CreateUserRequest
    ):
        hashed_password = self.__hashing.hash_password(password=req_data.password)
        hashed_email = self.__hashing.hash_for_search(data=req_data.email)

        encrypted_name = self.__encrytpion.encrypt(req_data.name)
        encrypted_email = self.__encrytpion.encrypt(req_data.email)

        user = entities.User(
            name=encrypted_name,
            email=encrypted_email,
            password=hashed_password,
            email_hash=hashed_email
        )

        new_user: entities.User = self.__repository.create(data=user)

        user_public = schemas.UserPublic(
            user_id=new_user.user_id,
            email=self.__encrytpion.decrypt(new_user.email),
            name=self.__encrytpion.decrypt(new_user.name),
            created_at=new_user.created_at
        )

        return user_public