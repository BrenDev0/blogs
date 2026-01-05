from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Blog(BaseModel):
    blog_id: Optional[UUID] = None
    user_id: UUID
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None