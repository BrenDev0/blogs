import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.blogs.application.use_cases.create import CreateBlog
from src.features.blogs.application.use_cases.delete import DeleteBlog
from src.features.blogs.application.use_cases.resource import GetBlogResource
from src.features.blogs.application.use_cases.collection import GetBlogsCollection
from src.features.blogs.application.use_cases.update import UpdateBlog
from src.features.blogs.dependencies.repositories import get_blog_repository
logger = logging.getLogger(__name__)

def get_create_blog_use_case() -> CreateBlog:
    try:
        instance_key = "create_blog_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")

    return use_case

def get_delete_blog_use_case() -> DeleteBlog:
    try:
        instance_key = "delete_blog_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = DeleteBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")

    return use_case

def get_blog_resource_use_case():
    try:
        instance_key = "get_blog_resource_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = GetBlogResource(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_blogs_collection_use_case() -> GetBlogsCollection:
    try:
        instance_key = "get_blogs_collection_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = GetBlogsCollection(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_update_blog_use_case() -> UpdateBlog:
    try:
        instance_key = "update_blog_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = UpdateBlog(
            repository=get_blog_repository()
        )

        Container.register(instance_key, use_case)

        logger.debug(f"{instance_key} registered")
    
    return use_case
    