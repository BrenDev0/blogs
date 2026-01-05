from pathlib import Path
import os
from src.features.email.domain.entities import Email
from src.features.email.application.services.sender import Sender

class VerificationEmail:
    def __init__(
        self,
        sender: Sender
    ):
        self.__from_addr = os.getenv("MAILER_USER")
        if not self.__from_addr:
            raise ValueError("Email variables not set")
        
        self.__subject = "Verificar Correo Electrónico"
        self.__sender = sender

    def __build_email( 
        self,
        to: str,
        verification_code: int
    ):
        template_path = Path(__file__).parent.parent.parent / "templates" / "verification.html"

        with open(template_path, 'r', encoding="utf-8") as f:
            template = f.read()
        
        email_body = template.replace('{{verification_code}}', str(verification_code))
        
        return Email(
            from_=self.__from_addr,
            to=to,
            subject=self.__subject,
            html=str(email_body)
        )
    
    def execute(
        self,
        to: str,
        verification_code: int
    ): 
        email = self.__build_email(
            to=to,
            verification_code=verification_code
        )

        self.__sender.execute(
            email=email
        )

        
        

        