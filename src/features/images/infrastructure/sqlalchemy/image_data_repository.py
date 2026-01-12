from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.features.images.domain.entities import Image
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base
class SqlAlchemyImage(Base):
    __tablename__ = "images" 

    image_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False)
    url = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

class SqlAlchemyImageRepository(SqlAlchemyDataRepository[Image, SqlAlchemyImage]):
    def __init__(self):
        super().__init__(SqlAlchemyImage)

    def _to_entity(self, model: SqlAlchemyImage):
        return Image(
            image_id=model.image_id,
            post_id=model.post_id,
            url=model.url,
            uploaded_at=model.uploaded_at
        )
    
    def _to_model(self, entity: Image):
        data = entity.model_dump(exclude={"image_id", "uploaded_at"} if not entity.image_id else set())
        return SqlAlchemyImage(**data)