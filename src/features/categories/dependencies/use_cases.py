import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.categories.application.use_cases import (
    create,
    delete,
    update,
    collection
)
from src.features.categories.dependencies.repositories import get_category_repository
from src.features.blogs.dependencies.repositories import get_blog_repository
logger = logging.getLogger(__name__)

def get_create_category_use_case() -> create.CreateCategory:
    try:
        instance_key = "create_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = create.CreateCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_delete_category_use_case() -> delete.DeleteCategory:
    try:
        instance_key = "delete_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = delete.DeleteCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_update_category_use_case() -> update.UpdateCategory:
    try:
        instance_key = "update_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = update.UpdateCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_category_collection_use_case() -> collection.GetCategoryCollection:
    try:
        instance_key = "category_collection_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = collection.GetCategoryCollection(
            blog_repository=get_blog_repository(),
            category_repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case