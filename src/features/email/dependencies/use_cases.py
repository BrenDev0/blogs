import logging
from src.di.domain.exceptions import DependencyNotRegistered
from src.di.container import Container
from src.features.email.dependencies.services import get_sender
from src.features.email.application.use_cases import verification, account_recovery
logger = logging.getLogger(__name__)


def get_verification_email_use_case() -> verification.VerificationEmail:
    try:
        instance_key = "verification_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = verification.VerificationEmail(
            sender=get_sender()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case

def get_account_recovery_email_use_case() -> account_recovery.AccoutRecovery:
    try:
        instance_key = "account_recovery_email_use_case"
        use_case = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        use_case = account_recovery.AccoutRecovery(
            sender=get_sender()
        )
        Container.register(instance_key, use_case)
        logger.debug(f"{instance_key} registered")
    
    return use_case
