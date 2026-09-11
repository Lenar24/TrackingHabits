"""
Модуль отвечает за загрузку и управление конфигурационными параметрами бота.

Использует библиотеку python-dotenv для загрузки переменных окружения
из общего .env файла в корне проекта.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Загружаем .env из корня проекта
# bot/core/config.py → bot/core → bot → project_root
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    # Fallback на стандартный поиск
    load_dotenv()


class Settings:
    """
    Класс для хранения конфигурационных параметров бота.

    Все параметры загружаются из переменных окружения (.env).
    """

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Bot
    MAX_BOT_TOKEN: Optional[str] = os.getenv("MAX_BOT_TOKEN")
    WEBHOOK_URL: Optional[str] = os.getenv("WEBHOOK_URL")
    BOT_WORKERS: int = int(os.getenv("BOT_WORKERS", "4"))
    BOT_PORT: int = int(os.getenv("BOT_PORT", "8001"))

    # API
    API_URL: str = os.getenv("API_URL", "http://backend:8000")

    # Database
    TOKEN_DB_PATH: str = os.getenv("TOKEN_DB_PATH", "bot_tokens.db")


settings = Settings()

# Проверка загрузки при отладке
if settings.DEBUG:
    print("=" * 50)
    print("🤖 Настройки бота:")
    print(f"  ENVIRONMENT: {settings.ENVIRONMENT}")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  API_URL: {settings.API_URL}")
    print(f"  MAX_BOT_TOKEN: {'✅ SET' if settings.MAX_BOT_TOKEN else '❌ NOT SET'}")
    print(f"  WEBHOOK_URL: {settings.WEBHOOK_URL or '❌ NOT SET'}")
    print(f"  BOT_PORT: {settings.BOT_PORT}")
    print("=" * 50)
