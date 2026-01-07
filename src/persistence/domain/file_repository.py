from abc import ABC, abstractmethod

class FileRepository(ABC):
    @abstractmethod
    def upload(self, key: str, file_bytes: bytes):
        raise NotImplementedError()
    
    def delete(self, key: str):
        raise NotImplementedError()