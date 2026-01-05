from sqlalchemy import Column, String, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from src.features.users.domain.entities import User
from src.persistence.infrastructure.sqlalchemy.data_repository import SqlAlchemyDataRepository, Base

class SqlAlchemyUser(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid4)
    email = Column(String, nullable=False)
    email_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class SqlAlchemyUserRepository(SqlAlchemyDataRepository[User, SqlAlchemyUser]):
    def __init__(self):
        super().__init__(SqlAlchemyUser)

    def _to_entity(self, model: SqlAlchemyUser):
        return User(
            user_id=model.user_id,
            email=model.email,
            email_hash=model.email_hash,
            password=model.password,
            is_admin=model.is_admin,
            created_at=model.created_at
        )
    
    def _to_model(self, entity: User):
        data = entity.model_dump(exclude={"user_id", "created_at"} if not entity.user_id else set())
        return SqlAlchemyUser(**data)