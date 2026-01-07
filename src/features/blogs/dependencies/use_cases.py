import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.blogs.application.use_cases import (
    create,
    collection,
    update,
    delete,
    resource
)
from src.features.blogs.dependencies.repositories import get_blog_repository
logger = logging.getLogger(__name__)

def get_create_blog_use_case() -> create.CreateBlog:
    try:
        instance_key = "create_blog_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = create.CreateBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")

    return use_case

def get_delete_blog_use_case() -> delete.DeleteBlog:
    try:
        instance_key = "delete_blog_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete.DeleteBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")

    return use_case

def get_blog_resource_use_case() -> resource.GetBlogResource:
    try:
        instance_key = "get_blog_resource_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = resource.GetBlogResource(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_blogs_collection_use_case() -> collection.GetBlogsCollection:
    try:
        instance_key = "get_blogs_collection_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = collection.GetBlogsCollection(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_blog_use_case() -> update.UpdateBlog:
    try:
        instance_key = "update_blog_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = update.UpdateBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")
    
    return use_case
    