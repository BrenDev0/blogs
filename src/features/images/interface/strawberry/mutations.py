import strawberry
import logging
from strawberry.file_uploads import Upload
from uuid import UUID
from typing import List
from src.app.interface.strawberry.middleware import user_auth
from src.app.domain.exceptions import GraphQlException
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from src.features.images.domain.exceptions import ImageUploadException, UnsuportedContentType
from src.features.images.interface.strawberry import types
from src.features.images.dependencies import business_rules, use_cases
logger = logging.getLogger(__name__)

@strawberry.type
class ImageMutaions:
    @strawberry.mutation(
        permission_classes=[user_auth.UserAuth],
        description="Upload an image for a blog post"
    )
    async def Upload(
        self,
        post_id: UUID,
        images: List[Upload],
        info: strawberry.Info
    ) -> List[types.UploadType]:
        user_id = info.context.get("user_id")
        use_case = use_cases.get_upload_image_use_case()
        content_rule = business_rules.get_supported_content_type_rule()
        uploaded_images = []
        errors = []
        try:
            for image in images:
                content_type = image.content_type
                filename = image.filename.lower().replace(" ", "_")

                content_rule.validate(content_type=content_type, filename=filename) # validate supported content type
                
                file_bytes = await image.read()
                
                try:
                    new_image = use_case.execute(
                        user_id=user_id,
                        post_id=post_id,
                        file_bytes=file_bytes,
                        content_type=content_type
                    )

                    uploaded_images.append(new_image)
                    
                except UnsuportedContentType as e:
                    errors.append(e)
                    continue
            
            return {
                "success": uploaded_images,
                "failed": errors
            }
                
        except (NotFoundException, PermissionsException, ImageUploadException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[user_auth.UserAuth],
        description="Delete and uploaded image"
    )
    def delete_image(
        self,
        image_id: UUID,
        info: strawberry.Info
    ):
        user_id = info.context.get("user_id")
        use_case = use_cases.get_delete_image_upload_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                image_id=image_id
            )
        
        except (NotFoundException, PermissionError) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        