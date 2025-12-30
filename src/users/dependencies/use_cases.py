import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.users.application.use_cases.create import CreateUser
from src.security.dependencies.services import get_encrytpion_service, get_hashing_service
from src.users.dependencies.repositories import get_user_repository
logger = logging.getLogger(__name__)

def get_create_user_use_case() -> CreateUser:
    try:
        instance_key = "create_user_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = CreateUser(
            repository=get_user_repository(),
            hashing=get_hashing_service(),
            encryption=get_encrytpion_service()
        )

        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case