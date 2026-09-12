"""
Модуль отвечает за загрузку и управление конфигурационными параметрами приложения.
Использует библиотеку python-dotenv для загрузки переменных окружения.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ✅ Загружаем .env.local если существует, иначе .env
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ENV_LOCAL = PROJECT_ROOT / ".env.local"
ENV_FILE = PROJECT_ROOT / ".env"

if ENV_LOCAL.exists():
    load_dotenv(dotenv_path=ENV_LOCAL)
    print(f"✅ Загружен .env.local")
else:
    load_dotenv(dotenv_path=ENV_FILE)
    print(f"✅ Загружен .env")


class Settings:
    """Класс для хранения всех конфигурационных параметров приложения."""

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgresql:postgresql@db:5432/habit_tracker"
    )
    DATABASE_POOL_SIZE = int(os.getenv("DATABASE_POOL_SIZE", "10"))
    DATABASE_MAX_OVERFLOW = int(os.getenv("DATABASE_MAX_OVERFLOW", "20"))

    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-min-32-characters")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Bot
    MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    BOT_WORKERS = int(os.getenv("BOT_WORKERS", "4"))

    # Internal API
    INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
    CORS_ALLOW_METHODS = os.getenv("CORS_ALLOW_METHODS", "*").split(",")
    CORS_ALLOW_HEADERS = os.getenv("CORS_ALLOW_HEADERS", "*").split(",")

    # Security
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

    # Redis
    REDIS_URL = os.getenv("REDIS_URL")
    REDIS_CACHE_EXPIRE = int(os.getenv("REDIS_CACHE_EXPIRE", "86400"))

    # Sentry
    SENTRY_DSN = os.getenv("SENTRY_DSN")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv(
        "LOG_FORMAT",
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    LOG_FILE = os.getenv("LOG_FILE")


# Создаем единственный экземпляр настроек
settings = Settings()

# Для отладки можно проверить загруженные значения
if settings.DEBUG:
    print("✅ Загрузка настроек:")
    print(f"  - ENVIRONMENT: {settings.ENVIRONMENT}")
    print(f"  - DATABASE_URL: {settings.DATABASE_URL}")
    print(f"  - MAX_BOT_TOKEN: {'✅ SET' if settings.MAX_BOT_TOKEN else '❌ NOT SET'}")
    print(f"  - WEBHOOK_URL: {settings.WEBHOOK_URL or '❌ NOT SET'}")
    print(f"  - SECRET_KEY: {'✅ SET' if settings.SECRET_KEY else '❌ NOT SET'}")
