import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered

from src.security.domain.services.web_token import WebTokenService
from src.security.infrastructure.jwt.web_token import JwtWebTokenService
from src.security.domain.services.hashing import HashingService
from src.security.infrastructure.bcrypt.hashing import BcryptHashingService
from src.security.domain.services.encryption import EncryptionService
from src.security.infrastructure.fernet.encryption import FernetEncryptionService
logger = logging.getLogger(__name__)

def get_web_token_service() -> WebTokenService:
    try:
        instance_key = "web_token_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = JwtWebTokenService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_hashing_service() -> HashingService:
    try:
        instance_key = "hashing_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = BcryptHashingService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service

def get_encrytpion_service() -> EncryptionService:
    try:
        instance_key = "encryption_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = FernetEncryptionService()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")

    return service