import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.comments.dependencies.repositories import get_comment_repository
from src.features.posts.dependencies.repositories import get_post_repository
from src.features.comments.application.use_cases import (
    collection_by_post,
    create,
    approve_all,
    approve_one,
    delete,
    collection_by_blog
)
logger = logging.getLogger(__name__)

def get_create_comment_use_case() -> create.CreateComment:
    try:
        instance_key = "create_comment_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = create.CreateComment(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_delete_comment_use_case() -> delete.DeleteComment:
    try:
        instance_key = "delete_comment_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = delete.DeleteComment(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_approve_comment_use_case() -> approve_one.ApproveComment:
    try:
        instance_key = "approve_comment_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = approve_one.ApproveComment(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_approve_all_comments_use_case() -> approve_all.ApproveAllComments:
    try:
        instance_key = "approve_all_comment_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = approve_all.ApproveAllComments(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case


def get_comment_collection_use_case() -> collection_by_post.CommentsCollectionByPost:
    try:
        instance_key = "comment_collection_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = collection_by_post.CommentsCollection(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case

def get_comment_collection_by_blog_use_case() -> collection_by_blog.CommentsCollection:
    try:
        instance_key = "comment_collection_by_blog_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = collection_by_blog.CommentsCollection(
            comment_repository=get_comment_repository(),
            post_repository=get_post_repository()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")

    return use_case