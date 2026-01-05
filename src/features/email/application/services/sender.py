import os
import smtplib
from email.message import EmailMessage
from src.features.email.domain.entities import Email
from src.features.email.domain.exceptions import EmailTransportException

class Sender:
    def __init__(self):
        self.host = os.getenv("MAILER_HOST")
        self.port = int(os.getenv("MAILER_PORT", 587))
        self.user = os.getenv("MAILER_USER")
        self.password = os.getenv("MAILER_PASSWORD")
        self.from_addr = os.getenv("MAILER_USER")


    def send(
        self,
        email: Email
    ):
        msg = EmailMessage()
        msg["From"] = email.from_
        msg["To"] = email.to
        msg["Subject"] = email.subject
        msg.set_content(email.html, subtype="html")
        msg["X-Mailgun-Track"] = "no"

        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)
                
        except Exception:
            raise EmailTransportException()