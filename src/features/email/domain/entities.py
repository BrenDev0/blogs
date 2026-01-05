from  pydantic import BaseModel, Field


class Email(BaseModel):
    from_: str
    to: str
    subject: str
    html: str