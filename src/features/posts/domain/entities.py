from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from src.features.blogs.domain.entities import Blog

class BlogPost(BaseModel):
    post_id: Optional[UUID] = None
    blog_id: UUID
    category_id: Optional[UUID] = None
    author: str
    title: str
    content_1: str
    content_2: Optional[str] = None
    published: Optional[bool] = False
    published_at: Optional[datetime] = None
    allow_comments: Optional[bool] = False
    created_at: Optional[datetime] = None
    blog: Optional[Blog] = None
