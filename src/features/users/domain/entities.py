from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class User(BaseModel): 
    user_id: Optional[UUID] = None
    email: str
    email_hash: str
    name: str
    password: str
    is_admin: bool
    created_at: Optional[datetime] = None