from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List, TypeVar
from src.persistence.domain.data_repository import DataRepository

T = TypeVar('T')
class CommentRepository(DataRepository):
    @abstractmethod
    def update_many(self, key: str, value: str | UUID, changes: dict) -> List[T] | None:
        raise NotImplementedError