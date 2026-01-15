from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.features.posts.domain.entities import BlogPost
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.blogs.infrastructure.sqlalchemy.blogs_repository import SqlAlchemyBlog
from src.features.blogs.domain.entities import Blog


class SqlAlchemyBlogPost(Base):
    __tablename__ = "posts"
    post_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.blog_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id", ondelete="SET NULL"), nullable=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content_1 = Column(String, nullable=True)
    content_2 = Column(String, nullable=True)
    allow_comments = Column(Boolean, nullable=False, default=False)
    published = Column(Boolean, nullable=False, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    blog = relationship("SqlAlchemyBlog")

class SqlAlchemyBlogPostRepository(SqlAlchemyDataRepository[BlogPost, SqlAlchemyBlogPost]):
    def __init__(self):
        super().__init__(SqlAlchemyBlogPost)

    def _to_entity(self, model: SqlAlchemyBlogPost):   
        return BlogPost(
            post_id=model.post_id,
            blog_id=model.blog_id,
            category_id=model.category_id,
            author=model.author,
            title=model.title,
            content_1=model.content_1,
            content_2=model.content_2,
            allow_comments=model.allow_comments,
            published=model.published,
            published_at=model.published_at,
            created_at=model.created_at,
            blog=self._blog_to_entity(model.blog)
        )
    
    def _blog_to_entity(self, model: SqlAlchemyBlog):
        if not model:
            return None
        
        return Blog(
            blog_id=model.blog_id,
            user_id=model.user_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: BlogPost):
        data = entity.model_dump(exclude={"post_id", "created_at", "blog"} if not entity.post_id else {"blog"})
        return SqlAlchemyBlogPost(**data)