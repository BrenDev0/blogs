from uuid import UUID
from typing import List
from src.persistence.domain.repositories import DataRepository
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
        user_id: UUID,
        blog_id: UUID,
        include_drafts: bool = False
    ):
        posts: List[entities.BlogPost] = self.__post_repository.get_many(
            key="blog_id",
            value=blog_id
        )

        if not posts:
            return []
        
        if str(posts[0].blog.user_id) != str(user_id):
            raise PermissionsException()
        
        if include_drafts:
            return [
                schemas.BlogPostPublic.model_validate(post, from_attributes=True) for post in posts
            ] 
        
        return [
            schemas.BlogPostPublic.model_validate(post, from_attributes=True) for post in posts if post.published
        ] 