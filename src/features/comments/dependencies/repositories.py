from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.comments.domain.comment_repository import CommentRepository
from src.features.comments.infrastructure.sqlalchemy.comments_repository import SqlAlchemyCommentsRepository

def get_comment_repository() ->  CommentRepository:
    try:
        instance_key = "comment_repostitory"
        repository = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        repository = SqlAlchemyCommentsRepository()