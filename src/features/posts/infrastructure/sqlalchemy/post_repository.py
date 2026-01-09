from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, func, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from src.features.posts.domain.entities import BlogPost
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.blogs.infrastructure.sqlalchemy.blogs_repository import SqlAlchemyBlog
from  src.features.blogs.domain.entities import Blog
from src.features.images.domain.entities import Image
from src.features.images.infrastructure.sqlalchemy.image_data_repository import SqlAlchemyImage

class SqlAlchemyBlogPost(Base):
    __tablename__ = "posts"
    post_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    blog_id = Column(UUID(as_uuid=True), ForeignKey("blogs.blog_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.category_id", ondelete="SET NULL"), nullable=True)
    author = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content_1 = Column(String, nullable=True)
    content_2 = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, default=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    images = relationship(
        "SqlAlchemyImage",
        primaryjoin="SqlAlchemyBlogPost.post_id==SqlAlchemyImage.post_id",
        lazy="select"
    )
    blog = relationship("SqlAlchemyBlog")

class SqlAlchemyBlogPostRepository(SqlAlchemyDataRepository[BlogPost, SqlAlchemyBlogPost]):
    def __init__(self):
        super().__init__(SqlAlchemyBlogPost)

    def _to_entity(self, model: SqlAlchemyBlogPost):
        images = [
            self._image_to_entity(model=image) for image in model.images
        ]
        
        return BlogPost(
            post_id=model.post_id,
            blog_id=model.blog_id,
            category_id=model.category_id,
            author=model.author,
            title=model.title,
            content_1=model.content_1,
            content_2=model.content_2,
            images=images,
            published=model.published,
            published_at=model.published_at,
            created_at=model.created_at,
            blog=self._blog_to_entity(model.blog)
        )
    
    def _image_to_entity(self, model: SqlAlchemyImage):
        return Image(
            image_id=model.image_id,
            post_id=model.image_id,
            url=model.url,
            uploaded_at=model.uploaded_at
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