import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.users.application.rules import (
    unique_email,
    update_password,
    user_exists
)
from src.features.users.dependencies.repositories import get_user_repository
from src.security.dependencies.services import get_hashing_service
logger = logging.getLogger(__name__)

def get_update_password_rule() -> update_password.UpdatePasswordRule:
    try:
        instance_key = "update_password_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = update_password.UpdatePasswordRule(
            repository=get_user_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.debug(f"{instance_key} registered")

    return business_rule

def get_unique_email_rule() -> unique_email.UniqueEmailRule:
    try:
        instance_key = "unique_email_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = unique_email.UniqueEmailRule(
            repository=get_user_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.debug(f"{instance_key} registered")

    return business_rule

def get_user_exists_rule() -> user_exists.UserExists:
    try:
        instance_key = "user_exists_rule"
        business_rule = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        business_rule = user_exists.UserExists(
            repository=get_user_repository(),
            hashing=get_hashing_service()
        )

        Container.register(instance_key, business_rule)
        logger.debug(f"{instance_key} registered")

    return business_rule
