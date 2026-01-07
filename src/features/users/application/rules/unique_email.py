from src.persistence.domain.data_repository import DataRepository
from src.security.domain.services.hashing import HashingService
from src.features.users.domain.exceptions import EmailInUseException

class UniqueEmailRule:
    def __init__(
        self,
        repository: DataRepository,
        hashing: HashingService
    ):
        self.__repository = repository
        self.__hashing = hashing
    
    def validate(
        self,
        email: str
    ):
        hashed_email = self.__hashing.hash_for_search(email)

        email_in_use = self.__repository.get_one(
            key="email_hash",
            value=hashed_email
        )

        if email_in_use:
            raise EmailInUseException()