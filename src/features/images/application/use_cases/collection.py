from uuid import UUID
from typing import Optional
from src.persistence.domain import exceptions as persitence_exceptions, data_repository
from src.security.domain.exceptions import PermissionsException
from src.features.images.domain import entities, exceptions as image_excepttions, schemas
from src.features.posts.domain.entities import BlogPost

class ImageCollection:
    def __init__(
        self,
        image_data_repository: data_repository.DataRepository,
        post_repository: data_repository.DataRepository

    ):
        self.__image_data_repository = image_data_repository
        self.__post_repository = post_repository

    def execte(
        self,
        post_id: UUID,
        user_id: UUID = None,
        include_drafts: bool = False
    ):
        post: BlogPost = self.__post_repository.get_one(
            key="post_id",
            value=post_id
        )

        if not post:
            raise persitence_exceptions.NotFoundException("Post not found")
        
        if include_drafts:
            if not user_id:
                raise ValueError("user_id needed for drafts")
            
            if str(post.blog.user_id) != str(user_id):
                raise PermissionsException()
            
        else: 
            if not post.published:
                raise PermissionsException()
        
        collection = self.__image_data_repository.get_many(
            key="post_id",
            value=post.post_id
        )

        return [
            schemas.ImagePublic.model_validate(image, from_attributes=True) for image in collection
        ] if collection else []

