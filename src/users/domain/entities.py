from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel): 
    user_id: Optional[str]
    email: str
    email_hash: str
    name: str
    password: str
    created_at: datetime