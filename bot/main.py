"""
Модуль является точкой входа для бота Habit Tracker.
Инициализирует FastAPI приложение с вебхуком для приема обновлений от Max API,
настраивает обработчики событий и управляет жизненным циклом бота.
"""

import asyncio
import json
import logging
import traceback

import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from maxapi import Bot

# Используем абсолютные импорты
from bot.core.config import settings
from bot.handlers import handle_bot_started, handle_message_callback, handle_message_created
from bot.services import APIClient

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация
MAX_BOT_TOKEN = settings.MAX_BOT_TOKEN
WEBHOOK_URL = settings.WEBHOOK_URL

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не задан в .env файле!")

bot = Bot(token=MAX_BOT_TOKEN)
client = APIClient()

# FASTAPI ПРИЛОЖЕНИЕ

app = FastAPI(title="Habit Tracker Bot Webhook")


@app.post("/webhook")
async def webhook(request: Request):
    """Основной эндпоинт для приема обновлений от Max API."""
    try:
        update_data = await request.json()
        update_type = update_data.get("update_type")
        logger.info("📨 Получен вебхук: %s", update_type)

        if update_type == "message_created":
            await handle_message_created(update_data, bot, client)
        elif update_type == "message_callback":
            await handle_message_callback(update_data, bot, client)
        elif update_type == "bot_started":
            await handle_bot_started(update_data, bot, client)
        else:
            logger.warning("⚠️ Неизвестный тип обновления: %s", update_type)

        return Response(status_code=200)
    except (httpx.HTTPError, json.JSONDecodeError, ValueError) as e:
        logger.error("❌ Ошибка обработки вебхука: %s", e)

        traceback.print_exc()
        return Response(status_code=500)


@app.get("/health")
async def health():
    """Эндпоинт для мониторинга состояния бота."""
    return {"status": "ok"}


# ЗАПУСК


async def set_webhook():
    """Регистрация вебхука в Max API."""
    url = "https://platform-api2.max.ru/subscriptions"
    headers = {"Authorization": f"{MAX_BOT_TOKEN}", "Content-Type": "application/json"}
    payload = {"url": f"{WEBHOOK_URL}", "events": ["message_created", "message_callback", "bot_started"]}

    async with httpx.AsyncClient(verify=False) as webhook_client:
        response = await webhook_client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info("✅ Вебхук установлен: %s", WEBHOOK_URL)
        else:
            logger.error("❌ Ошибка установки вебхука: %s", response.text)


async def main():
    """Основная функция запуска бота."""
    await set_webhook()
    print("🚀 Бот запущен с Webhook!")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")
    config = uvicorn.Config(app, host="0.0.0.0", port=8001, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
