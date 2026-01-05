from pydantic import BaseModel, EmailStr

class VerifyEmail(BaseModel):
    email: EmailStr
