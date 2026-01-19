import os
from pathlib import Path
from src.features.email.application.services.sender import Sender
from src.features.email.domain.entities import Email

class AccoutRecovery:
    def __init__(
        self,
        sender: Sender
    ):
        self.__from_addr = os.getenv("MAILER_USER")
        if not self.__from_addr:
            raise ValueError("Email variables not set")
        
        self.__sender = sender
        self.__subject = "Recuperación de Cuenta"

    
    def __build_email(
        self,
        to: str,
        token: str
    ):
        template_path = Path(__file__).parent.parent.parent / "templates" / "account_recovery.html"

        with open(template_path, 'r', encoding="utf-8") as f:
            template = f.read()
        
        recovery_link = ""
        email_body = template.replace('{{recovery_link}}', str(recovery_link))
        
        return Email(
            from_=self.__from_addr,
            to=to,
            subject=self.__subject,
            html=str(email_body)
        )

    def execute(
        self,
        to: str,
        token: str
    ):
        email = self.__build_email(
            to=to,
            token=token
        )

        self.__sender.send(
            email=email
        )