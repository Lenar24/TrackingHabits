import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
    API_URL = os.getenv("API_URL", "http://backend:8000")
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")


settings = Settings()
