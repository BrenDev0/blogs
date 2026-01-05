from sqlalchemy import Column, String, func, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.blogs.domain.entities import Blog

class SqlAlchemyBlog(Base):
    __tablename__ = "blogs"

    blog_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, default=None)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SqlAlchemyBlogRepository(SqlAlchemyDataRepository[Blog, SqlAlchemyBlog]):
    def __init__(self):
        super().__init__(SqlAlchemyBlog)
    
    def _to_entity(self, model: SqlAlchemyBlog):
        return Blog(
            blog_id=model.blog_id,
            user_id=model.user_id,
            name=model.name,
            description=model.description,
            created_at=model.created_at
        )

    def _to_model(self, entity: Blog):
        data = entity.model_dump(exclude={"blog_id", "created_at"} if not entity.blog_id else set())
        return SqlAlchemyBlog(**data)