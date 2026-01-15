import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.posts.application.use_cases import (
    collection,
    create,
    delete,
    update,
    like_post
)
from src.features.posts.dependencies.repositories import get_post_repository
from src.features.blogs.dependencies.repositories import get_blog_repository

logger = logging.getLogger(__name__)

def get_create_blog_post_use_case() -> create.CreateBlogPost:
    try:
        instance_key = "create_blog_post_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = create.CreateBlogPost(
            post_repository=get_post_repository(),
            blog_repositroy=get_blog_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_delete_blog_post_use_case() -> delete.DeleteBlogPost:
    try:
        instance_key = "delete_blog_post_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete.DeleteBlogPost(
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_blog_post_collection_use_case() -> collection.GetBlogPostCollection:
    try:
        instance_key = "blog_post_collection_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =collection.GetBlogPostCollection(
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_update_blog_post_use_case() -> update.UpdateBlogPost:
    try:
        instance_key = "update_blog_post_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = update.UpdateBlogPost(
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_like_post_use_case() -> like_post.LikePost:
    try:
        instance_key = "like_post_use_case",
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = like_post.LikePost(
            post_repository=get_post_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


