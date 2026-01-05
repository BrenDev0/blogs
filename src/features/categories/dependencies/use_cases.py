import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.categories.application.use_cases.create import CreateCategory
from src.features.categories.application.use_cases.delete import DeleteCategory
from src.features.categories.application.use_cases.update import UpdateCategory
from src.features.categories.application.use_cases.collection import GetCategoryCollection
from src.features.categories.dependencies.repositories import get_category_repository
logger = logging.getLogger(__name__)

def get_create_category_use_case() -> CreateCategory:
    try:
        instance_key = "create_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =CreateCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_delete_category_use_case() -> DeleteCategory:
    try:
        instance_key = "delete_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =DeleteCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_update_category_use_case() -> UpdateCategory:
    try:
        instance_key = "update_category_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =UpdateCategory(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_category_collection_use_case() -> GetCategoryCollection:
    try:
        instance_key = "category_collection_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case =GetCategoryCollection(
            repository=get_category_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case