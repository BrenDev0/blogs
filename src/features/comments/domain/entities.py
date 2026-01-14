from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class Comment(BaseModel):
    comment_id: Optional[UUID] = None
    post_id: UUID
    text: str
    approved: bool
    created_at: Optional[datetime] = None