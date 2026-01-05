import logging
from src.app.setup.db.engine import get_engine
from src.features.users.infrastructure.sqlalchemy.user_repository import SqlAlchemyUser

from src.persistence.infrastructure.sqlalchemy.data_repository import Base
logger = logging.getLogger(__name__)

def create_tables():
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        logger.info("tables created")
    
    except Exception as e:
        logger.error(str(e))