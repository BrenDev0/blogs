from pydantic import BaseModel
from typing import Optional
from  uuid import  UUID
from datetime import datetime

class Image(BaseModel):
    image_id: Optional[UUID] = None
    post_id: UUID
    url: Optional[str] = True
    uploaded_at: Optional[datetime] = None



