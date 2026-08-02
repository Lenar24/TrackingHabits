import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgresql:postgresql@db:5432/habit_tracker")

    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # Bot
    MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
    API_URL = os.getenv("API_URL", "http://localhost:8000")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")


settings = Settings()
