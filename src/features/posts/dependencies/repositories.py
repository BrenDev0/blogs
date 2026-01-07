import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence.domain.repositories import DataRepository
from src.features.posts.infrastructure.sqlalchemy.post_repository import SqlAlchemyBlogPostRepository
logger = logging.getLogger(__name__)

def get_post_repository() -> DataRepository:
    try:
        instance_key = "post_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = SqlAlchemyBlogPostRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")
    
    return repository


