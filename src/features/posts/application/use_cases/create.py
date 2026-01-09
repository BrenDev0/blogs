from uuid import UUID
from src.persistence.domain.data_repository import DataRepository
from src.features.blogs.domain.entities import Blog
from src.features.posts.domain import entities, schemas
from src.persistence.domain.exceptions import NotFoundException
from src.security.domain.exceptions import PermissionsException
from datetime import datetime, timezone

class CreateBlogPost:
    def __init__(
        self,
        post_repository: DataRepository,
        blog_repositroy: DataRepository
    ):
        self.__post_repository = post_repository
        self.__blog_repository = blog_repositroy

    
    def execute(
        self,
        user_id: UUID,
        blog_id: UUID,
        req_data: schemas.CreateBlogPostRequest
    ): 
        blog: Blog = self.__blog_repository.get_one(
            key="blog_id",
            value=blog_id
        )

        if not blog:
            raise NotFoundException("Blog not found")
        
        if str(blog.user_id) != str(user_id):
            raise PermissionsException()
        

        req_data_to_dict = req_data.model_dump(by_alias=False)

        is_publishing = req_data_to_dict.get("published")

        if is_publishing:
            publishing_date = datetime.now(timezone.utc)
            req_data_to_dict["published_at"] = publishing_date

        data = entities.BlogPost(
            blog_id=blog_id,
            **req_data_to_dict
        )  

        new_post: entities.BlogPost = self.__post_repository.create(
            data=data
        )

        return schemas.BlogPostPublic.model_validate(new_post, from_attributes=True)