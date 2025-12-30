from abc import ABC, abstractmethod
from typing import Dict, Any

class WebTokenService(ABC):
    @abstractmethod
    def decode(
        self,
        token: str
    ):
        raise NotImplementedError
    
    @abstractmethod
    def generate(
        self,
        payload: Dict[str, Any],
        expiration: int = 900
    ) -> str:
        raise NotImplementedError