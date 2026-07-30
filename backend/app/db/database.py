from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
)

def create_db_and_tables():
    # ❗ Phase III me Alembic handle karega
    pass

def get_session():
    return Session(engine)