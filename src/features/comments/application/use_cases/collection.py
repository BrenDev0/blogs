from uuid import UUID
from src.persistence.domain import data_repository, exceptions
from src.features.comments.domain import entities, schemas

class CommentsCollection:
    def __init__(
        self,
        repository: data_repository.DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        post_id: UUID,
        user_id: UUID = None,
        include_unapproved: bool = False  
    ):
        pass