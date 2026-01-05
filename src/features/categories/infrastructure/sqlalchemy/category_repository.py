from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base
from src.features.categories.domain.entities import Category

class SqlAlchemyCategory(Base):
    __tablename__ = "categories"

    category_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    create_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SqlAlcheyCategoryRepository(SqlAlchemyDataRepository[Category, SqlAlchemyCategory]):
    def __init__(self):
        super().__init__(SqlAlchemyCategory)

    def _to_entity(self, model: SqlAlchemyCategory):
        return Category(
            category_id=model.category_id,
            user_id=model.user_id,
            name=model.name,
            created_at=model.create_at
        )
    
    def _to_model(self, entity: Category):
        data = entity.model_dump(exclude={"category_id", "created_at"} if not entity.category_id else set())
        return SqlAlchemyCategory(**data)