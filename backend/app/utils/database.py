"""
Модуль отвечает за настройку подключения к базе данных,
создание сессий и управление соединениями.
Использует SQLAlchemy ORM для работы с PostgreSQL базой данных.
Предоставляет функции для получения сессий базы данных
с автоматическим управлением жизненным циклом.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Генератор для получения сессии базы данных с автоматическим управлением."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
