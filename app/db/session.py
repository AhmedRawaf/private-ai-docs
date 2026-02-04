from __future__ import annotations

from sqlalchemy import create_engine
from sqlmodel import Session

from app.core.config import get_settings


settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    future=True,
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session

