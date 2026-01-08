from uuid import  UUID
from src.persistence.domain import file_repository

class UploadImage:
    def __init__(
        self,
        file_repository: file_repository.FileRepository
    ):
        self.__file_repository = file_repository

    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        content_id: UUID,
        image_id: UUID,
        file_bytes: bytes
    ):
        key = f"{user_id}/blogs/{blog_id}/{content_id}/{image_id}"
        
        return self.__file_repository.upload(
            key=key,
            file_bytes=file_bytes
        )
    

