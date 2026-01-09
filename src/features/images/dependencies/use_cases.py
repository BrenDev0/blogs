import logging
from src.di.container import Container
from src.di.domain.exceptions import  DependencyNotRegistered
from src.features.images.application.use_cases import (
    delete,
    upload_post_image
)
from src.features.images.dependencies.repositories import get_image_file_repository
logger = logging.getLogger(__name__)

def get_upload_image_use_case() -> upload_post_image.UploadBlogPostImage:
    try: 
        instance_key = "upload_image_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = upload_post_image.UploadBlogPostImage(
            file_repository=get_image_file_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_delete_image_upload_use_case() -> delete.DeleteImageUpload:
    try: 
        instance_key = "delete_image_upload_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = delete.DeleteImageUpload(
            file_repository=get_image_file_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case