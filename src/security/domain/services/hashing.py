from abc import ABC, abstractmethod

class HashingService(ABC):
    @abstractmethod
    def hash_for_search(self, data: str) -> str:
       raise NotImplementedError()

    @abstractmethod
    def hash_password(self, password: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def compare_password(
        password: str, 
        hashed_password: str, 
        detail: str = "Incorrect password", 
        throw_error: bool = True
    ) -> bool:
        raise NotImplementedError()