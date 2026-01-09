from uuid import  UUID
from src.persistence.domain import file_repository, data_repository, exceptions
from src.security.domain.exceptions import PermissionsException
from src.features.images.domain import entities, schemas, exceptions as image_exceptions
from src.features.posts.domain.entities import BlogPost

class UploadBlogPostImage:
    def __init__(
        self,
        file_repository: file_repository.FileRepository,
        images_data_repository: data_repository.DataRepository,
        posts_data_repository: data_repository.DataRepository
    ):
        self.__file_repository = file_repository
        self.__images_data_repository = images_data_repository
        self.__posts_data_repository = posts_data_repository

    def execute(
        self,
        user_id: UUID,
        post_id: UUID,
        file_bytes: bytes
    ):
        post: BlogPost = self.__posts_data_repository.get_one(
            key="post_id",
            value=post_id
        )
        
        if not post:
            raise exceptions.NotFoundException("Post not found")
        
        if str(post.blog.user_id) != str(user_id):
            raise PermissionsException()

        data = entities.Image(
            post_id=post_id,
        )

        new_image_data: entities.Image = self.__images_data_repository.create(
            data=data
        )
        
        key = f"{user_id}/blogs/{post.blog_id}/{new_image_data.post_id}/{new_image_data.image_id}"
        
        try:
            url = self.__file_repository.upload(
                key=key,
                file_bytes=file_bytes
            )
        
        except Exception:
            self.__images_data_repository.delete(
                key="image_id",
                value=new_image_data.image_id
            )

            raise image_exceptions.ImageUploadException()

        changes = {
            "url": url
        }

        updated_image: entities.Image = self.__images_data_repository.update(
            key="image_id",
            value=new_image_data.image_id,
            changes=changes
        ) 

        return schemas.ImagePublic.model_validate(updated_image, from_attributes=True)




    

