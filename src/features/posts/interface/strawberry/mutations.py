import logging
import strawberry
from strawberry.file_uploads import Upload
from typing import List
from uuid import UUID
from src.app.domain.exceptions import GraphQlException
from src.app.interface.strawberry.decorators.req_validation import validate_input_to_model
from src.app.interface.strawberry.middleware.user_auth import UserAuth
from src.persistence.domain.exceptions import NotFoundException, UpdateFieldsException
from src.features.images.domain.exceptions import ImageUploadException
from src.security.domain.exceptions import PermissionsException
from src.features.posts.interface.strawberry import types, inputs
from src.features.posts.dependencies.use_cases import (
    get_create_blog_post_use_case,
    get_delete_blog_post_use_case,
    get_update_blog_post_use_case,
    get_like_post_use_case
)
from src.features.images.dependencies import use_cases, business_rules
from src.features.images.domain.exceptions import UnsuportedContentType
logger = logging.getLogger(__name__)

@strawberry.type
class BlogPostMutations:
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Create a blog post, Images is an optional field if included images will be uploaded and taged with the post_id"
    )
    @validate_input_to_model
    async def create_blog_post(
        self,
        blog_id: UUID,
        info: strawberry.Info,
        input: inputs.CreateBlogPostInput,
        images: List[Upload] | None = None,
    ) -> types.BlogPostType | types.BlogPostWithUploadType:
        user_id = info.context.get("user_id")
        use_case = get_create_blog_post_use_case()

        try:
            new_post = use_case.execute(
                user_id=user_id,
                blog_id=blog_id,
                req_data=input
            )

            if images:
                upload_use_case = use_cases.get_upload_image_use_case()
                uploaded_images = []
                errors = []
                
                for image in images:
                    content_type = image.content_type
                    filename = image.filename.lower().replace(" ", "_")

                    business_rules.content_rule.validate(content_type=content_type, filename=filename) # validate supported content type
                    
                    file_bytes = await image.read()
                    
                    try:
                        new_image = upload_use_case.execute(
                            user_id=user_id,
                            post_id=new_post.post_id,
                            file_bytes=file_bytes,
                            content_type=content_type
                        )

                        uploaded_images.append(new_image)
                        
                    except UnsuportedContentType as e:
                        errors.append(e)
                        continue
                return types.BlogPostWithUploadType(
                    post=new_post,
                    images=uploaded_images,
                    failed_uploads=errors
                )

            return new_post
        
        except (PermissionsException, NotFoundException, ImageUploadException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Update blog post by id"
    )
    @validate_input_to_model
    def update_blog_post(
        self,
        post_id: UUID,
        info: strawberry.Info,
        input: inputs.UpdateBlogPostInput
    ) -> types.BlogPostType:
        user_id = info.context.get("user_id")
        use_case = get_update_blog_post_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                post_id=post_id,
                changes=input
            )
        
        except (PermissionsException, NotFoundException, UpdateFieldsException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
        
    @strawberry.mutation(
        permission_classes=[UserAuth],
        description="Delete blog post by id"
    )
    def delete_blog_post(
        self,
        post_id: UUID,
        info: strawberry.Info
    ) -> types.BlogPostType:
        user_id = info.context.get("user_id")
        use_case = get_delete_blog_post_use_case()

        try:
            return use_case.execute(
                user_id=user_id,
                post_id=post_id
            )
        
        except (PermissionsException, NotFoundException) as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()
    
    @strawberry.mutation(
        description="Like blog post **UNPROTECTED**"
    )
    def public_like_post(
        self,
        post_id: UUID
    ) -> types.BlogPostType:
        try:
            use_case = get_like_post_use_case()

            return use_case.execute(
                post_id=post_id
            )
        
        except NotFoundException as e:
            raise GraphQlException(str(e))
        
        except Exception as e:
            logger.error(str(e))
            raise GraphQlException()