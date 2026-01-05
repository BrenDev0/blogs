from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Category(BaseModel):
    category_id: UUID
    user_id: UUID
    name: str