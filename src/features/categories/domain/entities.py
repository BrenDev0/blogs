from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class Category(BaseModel):
    category_id: Optional[UUID] = None
    user_id: UUID
    name: str
    created_at: Optional[datetime] = None