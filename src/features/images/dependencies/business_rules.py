import logging
from src.di.container import Container
from src.di.domain.exceptions import DependencyNotRegistered
from src.features.images.application.rules import supported_content_type
logger = logging.getLogger(__name__)

def get_supported_content_type_rule() -> supported_content_type.SupportedContenType:
    try:
        instance_key = "supported_content_type_rule"
        rule = Container.resolve(instance_key)

    except DependencyNotRegistered:
        rule = supported_content_type.SupportedContenType()
        Container.register(instance_key, rule)
        logger.debug(f"{instance_key} registered")

    return rule
