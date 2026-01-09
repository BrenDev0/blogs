from uuid import UUID
from typing import List
from src.persistence.domain.data_repository import DataRepository
from src.security.domain.exceptions import PermissionsException
from src.features.posts.domain import entities, schemas

class GetBlogPostCollection:
    def __init__(
        self,
        post_repository: DataRepository
    ):
        self.__post_repository = post_repository

    
    def execute(
        self,
        blog_id: UUID,
        user_id: UUID = None,
        category_id: UUID = None,
        per_page: int = 10,
        page_number: int = 1,
        include_drafts: bool = False
    ):
        offset = (page_number - 1) * per_page

        if category_id:
            posts: List[entities.BlogPost] = self.__post_repository.get_many(
                key="blog_id",
                value=blog_id,
                secondary_key="category_id",
                secondary_value=category_id,
                limit=per_page,
                offset=offset
            )
        
        else:
            posts: List[entities.BlogPost] = self.__post_repository.get_many(
            key="blog_id",
            value=blog_id,
            limit=per_page,
            offset=offset
        )

        if not posts:
            return []
        
        if include_drafts:
            if str(posts[0].blog.user_id) != str(user_id):
                raise PermissionsException()
            
            return [
                schemas.BlogPostPublic.model_validate(post, from_attributes=True) for post in posts
            ] 
        
        return [
            schemas.BlogPostPublic.model_validate(post, from_attributes=True) for post in posts if post.published
        ] 