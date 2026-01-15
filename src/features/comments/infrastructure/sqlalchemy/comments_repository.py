from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, func, update, select
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.features.comments.domain import entities, comment_repository
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base

class SqlAlchemyComment(Base):
    __tablename__ = "comments"

    comment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    text = Column(String, nullable=False)
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SqlAlchemyCommentsRepository(
    SqlAlchemyDataRepository[entities.Comment, SqlAlchemyComment], 
    comment_repository.CommentRepository
):
    def __init__(self):
        super().__init__(SqlAlchemyComment)

    def update_many(self, key, value, changes):
        stmt = update(self.model).where(getattr(self.model, key) == value).values(**changes).returning(*self.model.__table__.c)

        with self._get_session() as db:
            result = db.execute(stmt)
            db.commit()
            
            updated_rows = result.fetchall()
            
            if not updated_rows:
                return None
            
            # Create model instance and convert to entity
            updated_models = [
                self.model(**row._mapping) for row in updated_rows
            ]
            
            return [
                self._to_entity(model) for model in updated_models
            ]

    
    def _to_entity(self, model: SqlAlchemyComment):
        return entities.Comment(
            comment_id=model.comment_id,
            post_id=model.post_id,
            text=model.text,
            approved=model.approved,
            created_at=model.created_at
        )
    
    def _to_model(self, entity):
        data = entity.model_dump(exclude={"comment_id", "created_at"} if not entity.comment_id else set())

        return SqlAlchemyComment(**data)