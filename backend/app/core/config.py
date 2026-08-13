"""
Модуль отвечает за загрузку и управление конфигурационными параметрами приложения.
Использует библиотеку python-dotenv для загрузки переменных окружения
из файла .env и предоставляет единый объект Settings для доступа к настройкам во всем приложении.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:  # pylint: disable=too-few-public-methods
    """Класс для хранения всех конфигурационных параметров приложения со значениями по умолчанию."""

    # Database. Строка подключения к PostgreSQL базе данных.
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgresql:postgresql@db:5432/habit_tracker")

    # JWT. Секретный ключ для подписи JWT токенов.
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Bot. Токен для авторизации в Max.
    MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    # URL для вебхука бота. Публичный URL, доступный из интернета.
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")


settings = Settings()
