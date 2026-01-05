import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence.domain.repositories import DataRepository
from src.features.categories.infrastructure.sqlalchemy.category_repository import SqlAlcheyCategoryRepository
logger = logging.getLogger(__name__)

def get_category_repository() -> DataRepository:
    try:
        instance_key = "category_repository"
        repository = Container.resolve(instance_key)
        
    except DependencyNotRegistered:
        repository = SqlAlcheyCategoryRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository
