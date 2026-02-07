from sqlmodel import SQLModel, create_engine
from app.core.config import Settings

_engine = None


def get_engine(settings: Settings):
    global _engine
    if _engine is None:
        _engine = create_engine(settings.database_url, pool_pre_ping=True)
    return _engine


def create_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)
