import logging
from uuid import UUID
from src.persistence.domain import file_repository, data_repository, exceptions as persistance_exceptions
from src.features.images.domain import schemas, entities, exceptions as image_exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain.entities import BlogPost
logger = logging.getLogger(__name__)

class DeleteImageUpload:
    def __init__(
        self,
        image_file_repository: file_repository.FileRepository,
        image_data_repository: data_repository.DataRepository,
        post_data_repository: data_repository.DataRepository
    ):
        self.__image_file_repository = image_file_repository
        self.__image_data_repository = image_data_repository
        self.__post_data_repository = post_data_repository

    def execute(
        self,
        user_id: UUID,
        image_id: UUID
    ): 
        image: entities.Image = self.__image_data_repository.get_one(
            key="image_id",
            value=image_id
        )

        if not image:
            raise persistance_exceptions.NotFoundException("Image not found")
        
        post: BlogPost = self.__post_data_repository.get_one(
            key="post_id",
            value=image.post_id
        )

        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()
        
        key = f"{user_id}/blogs/{post.blog_id}/{post.post_id}/{image.image_id}"

        try:
            self.__image_file_repository.delete(key=key)

        except Exception as e:
            logger.error(str(e))
            raise image_exceptions.ImageUploadException()
        
        deleted_image: entities.Image = self.__image_data_repository.delete(
            key="image_id",
            value=image.image_id
        )

        return schemas.ImagePublic.model_validate(deleted_image, from_attributes=True)