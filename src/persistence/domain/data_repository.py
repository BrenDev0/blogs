from abc  import ABC, abstractmethod
from uuid import UUID
from typing  import List, Dict, Any, TypeVar, Generic, Union

T = TypeVar('T')

class DataRepository(ABC, Generic[T]):
    @abstractmethod
    def create(self, data: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_one(self, key: str, value: Union[str, UUID]) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def get_many(
        self,
        key: str, 
        value: Union[str, UUID, List[Union[str, UUID]]],
        secondary_key: str = None,
        secondary_value: Union[str, UUID] = None, 
        limit: int = None, 
        offset: int = 0,
        order_by=None, 
        desc: bool = False
    ) -> List[T]:
        raise NotImplementedError
    
    @abstractmethod
    def get_all(self,) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, key: str, value: Union[str, UUID], changes: Dict[str, Any]) -> T | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str, value: Union[str, UUID]) -> List[T] | T | None:
        raise NotImplementedError
    