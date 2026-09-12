"""
Модуль настройки логирования приложения.
"""

import logging
import sys
from pathlib import Path

from .config import settings


def setup_logging():
    """Настройка логирования для приложения."""

    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    log_format = settings.LOG_FORMAT

    # Базовый конфиг
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Добавление файлового логгера (опционально)
    if settings.LOG_FILE:
        log_path = Path(settings.LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(settings.LOG_FILE)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)

    # Настройка логгеров для библиотек
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)

    # Создание логгера приложения
    logger = logging.getLogger("habit_tracker")
    logger.setLevel(log_level)

    logger.info(f"Logging configured with level: {settings.LOG_LEVEL}")
