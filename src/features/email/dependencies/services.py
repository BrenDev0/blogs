import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.email.application.services import sender
logger = logging.getLogger(__name__)


def get_sender() -> sender.Sender:
    try:
        instance_key = "email_sender"
        service = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        service = sender.Sender()
        Container.register(instance_key, service)
        logger.debug(f"{instance_key} registered")
    
    return service