import os
import logging
from sqlalchemy import create_engine, Engine

logger = logging.getLogger(__name__)

def get_engine() -> Engine:
    DB_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DB_URL, pool_pre_ping=True)  

    return engine

