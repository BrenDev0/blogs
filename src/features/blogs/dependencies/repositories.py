import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.persistence.domain.data_repository import DataRepository
from src.features.blogs.infrastructure.sqlalchemy.blogs_repository import SqlAlchemyBlogRepository
logger = logging.getLogger(__name__)

def get_blog_repository() -> DataRepository:
    try:
        instance_key = "blog_repository"
        repository = Container.resolve(instance_key)
        
    except DependencyNotRegistered:
        repository = SqlAlchemyBlogRepository()
        Container.register(instance_key, repository)
        logger.debug(f"{instance_key} registered")

    return repository
