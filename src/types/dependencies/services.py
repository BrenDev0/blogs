import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.types.application.services import type_validation
logger = logging.getLogger(__name__)

def get_type_validation_service() -> type_validation.TypeValidationService:
    try:
        isinstance_key = "type_validation_service"
        service = Container.resolve(isinstance_key)
    
    except DependencyNotRegistered:
        service =  type_validation.TypeValidationService()
        Container.register(isinstance_key, service)
        logger.debug(f"{isinstance_key} registered")
    
    return service