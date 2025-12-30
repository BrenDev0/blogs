import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.persistence.domain.repositories import DataRepository
from src.users.infrastructure.sqlalchemy.user_repository import SqlAlchemyUserRepository
logger = logging.getLogger(__name__)

def get_user_repository() -> DataRepository:
    try:
        instance_key = "user_repository"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyUserRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")
    
    return repository
