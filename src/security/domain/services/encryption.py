from abc import ABC, abstractmethod
from typing import Union

class EncryptionService(ABC):
    @abstractmethod
    def encrypt(self, data: Union[str, int]) -> str:
        raise NotImplementedError()

    @abstractmethod
    def decrypt(self, data: Union[str, int]) -> str:
        raise NotImplementedError()