from uuid import UUID
from src.persistence.domain.file_repository import FileRepository

class DeleteImageUpload:
    def __init__(
        self,
        file_repository: FileRepository
    ):
        self.__file_repository = file_repository

    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        content_id: UUID,
        image_id: UUID
    ): 
        key = f"{user_id}/blogs/{blog_id}/{content_id}/{image_id}"

        return self.__file_repository.delete(key=key)