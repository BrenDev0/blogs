from src.persistence.domain import exceptions, data_repository
from src.security.domain.services import hashing
from src.features.users.domain import entities, schemas

class UserExists:
    def __init__(
        self,
        repository: data_repository.DataRepository,
        hashing: hashing.HashingService
    ):
        self.__user_repository = repository
        self.__hashing = hashing

    def validate(
        self,
        email: str
    ):
        hashed_email = self.__hashing.hash_for_search(data=email)

        user_exists: entities.User = self.__user_repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if not user_exists:
            raise exceptions.NotFoundException("Incorrect email")
        

        return user_exists