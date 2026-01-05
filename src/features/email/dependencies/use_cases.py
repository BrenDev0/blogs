import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.email.dependencies.services import get_sender
from src.features.email.application.use_cases.verification import VerificationEmail
logger = logging.getLogger(__name__)


def get_verification_email_use_case() -> VerificationEmail:
    try:
        instance_key = "verification_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = VerificationEmail(
            sender=get_sender()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case
