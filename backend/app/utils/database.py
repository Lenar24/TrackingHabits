"""
Модуль для настройки и управления подключением к базе данных.
"""

import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, event, text  # ✅ Добавлен text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from ..core.config import settings

logger = logging.getLogger(__name__)

# Настройка движка БД
try:
    engine = create_engine(
        settings.DATABASE_URL,
        poolclass=QueuePool,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,
        echo=settings.DEBUG,
    )

    # ✅ Проверка подключения с text()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Соединение с базой данных успешно установлено")
    except Exception as e:
        logger.warning(f"⚠️ База данных временно недоступна: {e}")
        # НЕ падаем! Продолжаем работу

except Exception as e:
    logger.error(f"❌ Не удалось создать engine: {e}")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Генератор для получения сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Ошибка базы данных: {e}")
        raise
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """
    Контекстный менеджер для работы с БД.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Инициализация базы данных (создание таблиц).
    """
    from ..models import Base

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Таблицы базы данных успешно созданы")
    except Exception as e:
        logger.error(f"❌ Не удалось создать таблицы: {e}")
        raise


@event.listens_for(engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Логирование SQL запросов (для отладки)."""
    if settings.DEBUG:
        logger.debug(f"SQL: {statement}")
        if parameters:
            logger.debug(f"Params: {parameters}")
