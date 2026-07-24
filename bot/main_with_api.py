import os
import asyncio
import logging
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, Request, Response
import uvicorn

from maxapi import Bot
from maxapi.types import MessageCreated, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
API_URL = os.getenv("API_URL", "http://backend:8000")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("WEBHOOK_URL не задан в .env файле!")

bot = Bot(token=MAX_BOT_TOKEN)
client = httpx.AsyncClient(timeout=30.0, verify=False)


def create_keyboard_attachment():
    """Создает клавиатуру через InlineKeyboardBuilder"""
    builder = InlineKeyboardBuilder()
    builder.add(
        {"type": "callback", "text": "📋 Мои привычки", "payload": "my_habits"},
        {"type": "callback", "text": "➕ Добавить привычку", "payload": "add_habit"}
    )
    builder.adjust(1)
    return [builder.as_markup()]


async def send_welcome(chat_id):
    """Отправляет приветственное сообщение с кнопками"""
    await bot.send_message(
        chat_id=chat_id,
        text=(
            "🌟 Добро пожаловать в Трекер привычек!\n\n"
            "Я помогу вам:\n"
            "✅ Отслеживать ежедневные привычки\n"
            "📊 Видеть прогресс\n"
            "⏰ Напоминать о задачах\n\n"
            "Выберите действие:"
        ),
        attachments=create_keyboard_attachment()
    )


async def get_or_create_user(user_id: int, username: str = None, chat_id: int = None):
    """Получить или создать пользователя в БД"""
    response = await client.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        user_data = response.json()
        if chat_id and user_data.get('chat_id') != chat_id:
            await client.put(
                f"{API_URL}/users/{user_id}/chat_id",
                json={"chat_id": chat_id}
            )
        return user_data

    response = await client.post(
        f"{API_URL}/users/",
        json={"user_id": user_id, "username": username, "chat_id": chat_id}
    )
    if response.status_code == 200:
        return response.json()

    logger.error(f"❌ Ошибка создания пользователя: {response.text}")
    return None


async def get_user_habits(user_id: int):
    """Получить привычки пользователя из БД"""
    response = await client.get(f"{API_URL}/habits/{user_id}")
    if response.status_code == 200:
        return response.json()
    return []


async def add_user_habit(user_id: int, habit_name: str):
    """Добавить привычку пользователя в БД"""
    response = await client.post(
        f"{API_URL}/habits/",
        json={"user_id": user_id, "name": habit_name}
    )
    if response.status_code == 200:
        return response.json()
    logger.error(f"❌ Ошибка добавления привычки: {response.text}")
    return None


# ============================================
# ОБРАБОТЧИКИ СОБЫТИЙ (вручную)
# ============================================

async def handle_bot_started(update_data: dict):
    """Обработчик события bot_started"""
    try:
        chat_id = update_data.get('chat_id')
        user_id = update_data.get('user_id')
        logger.info(f"✅ Событие bot_started: chat_id={chat_id}")
        await get_or_create_user(user_id, None, chat_id)
        await send_welcome(chat_id)
    except Exception as e:
        logger.error(f"❌ Ошибка в bot_started: {e}")


async def handle_message_created(update_data: dict):
    """Обработчик события message_created"""
    try:
        message_data = update_data.get('message')
        if not message_data:
            return

        chat_id = message_data.get('recipient', {}).get('chat_id')
        user_id = message_data.get('sender', {}).get('user_id')
        username = message_data.get('sender', {}).get('first_name')
        text = message_data.get('body', {}).get('text')

        logger.info(f"📩 Получено сообщение от {user_id} в чат {chat_id}")

        if not chat_id or not user_id:
            logger.warning("⚠️ Не удалось получить chat_id или user_id")
            return

        await get_or_create_user(user_id, username, chat_id)

        if not text:
            return

        logger.info(f"💬 Текст: {text}")

        if text.lower() in ["начать", "/start", "start"]:
            await send_welcome(chat_id)
            return

        if text.startswith('/'):
            return

        habit = await add_user_habit(user_id, text)
        if habit:
            habits_count = len(await get_user_habits(user_id))
            await bot.send_message(
                chat_id=chat_id,
                text=f"✅ Привычка «{text}» добавлена!\n"
                     f"📋 Всего привычек: {habits_count}"
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Не удалось добавить привычку. Попробуйте позже."
            )
    except Exception as e:
        logger.error(f"❌ Ошибка в message_created: {e}")


async def handle_message_callback(update_data: dict):
    """Обработчик события message_callback"""
    try:
        callback = update_data.get('callback')
        if not callback:
            return

        payload = callback.get('payload')
        user_id = callback.get('user', {}).get('user_id')
        message = update_data.get('message', {})
        chat_id = message.get('recipient', {}).get('chat_id')

        logger.info(f"🔘 Получен callback: {payload}")

        if not chat_id or not user_id:
            return

        await get_or_create_user(user_id, None, chat_id)

        if payload == "my_habits":
            habits = await get_user_habits(user_id)
            if not habits:
                await bot.send_message(
                    chat_id=chat_id,
                    text="📋 У вас пока нет привычек. Нажмите «➕ Добавить привычку»."
                )
            else:
                habits_text = "📋 Ваши привычки:\n\n"
                for i, habit in enumerate(habits, 1):
                    status = "✅" if habit.get("is_active", True) else "❌"
                    habits_text += f"{i}. {habit['name']} {status} ({habit.get('days_completed', 0)} дн.)\n"
                await bot.send_message(
                    chat_id=chat_id,
                    text=habits_text
                )
        elif payload == "add_habit":
            await bot.send_message(
                chat_id=chat_id,
                text="✏️ Введите название новой привычки:"
            )
    except Exception as e:
        logger.error(f"❌ Ошибка в message_callback: {e}")


# ============================================
# FASTAPI ПРИЛОЖЕНИЕ ДЛЯ WEBHOOK
# ============================================

app = FastAPI(title="Habit Tracker Bot Webhook")


@app.post("/webhook")
async def webhook(request: Request):
    """Эндпоинт для приёма вебхуков от MAX"""
    try:
        update_data = await request.json()
        update_type = update_data.get('update_type')
        logger.info(f"📨 Получен вебхук: {update_type}")

        # Обрабатываем события вручную
        if update_type == 'message_created':
            await handle_message_created(update_data)
        elif update_type == 'message_callback':
            await handle_message_callback(update_data)
        elif update_type == 'bot_started':
            await handle_bot_started(update_data)
        else:
            logger.warning(f"⚠️ Неизвестный тип обновления: {update_type}")

        return Response(status_code=200)
    except Exception as e:
        logger.error(f"❌ Ошибка обработки вебхука: {e}")
        import traceback
        traceback.print_exc()
        return Response(status_code=500)


@app.get("/health")
async def health():
    """Проверка здоровья сервиса"""
    return {"status": "ok"}


# ============================================
# ЗАПУСК
# ============================================

async def set_webhook():
    """Устанавливает вебхук для бота"""
    url = "https://platform-api2.max.ru/subscriptions"
    headers = {
        "Authorization": f"{MAX_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": f"{WEBHOOK_URL}",
        "events": ["message_created", "message_callback", "bot_started"]
    }

    async with httpx.AsyncClient(verify=False) as webhook_client:
        response = await webhook_client.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            logger.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")
        else:
            logger.error(f"❌ Ошибка установки вебхука: {response.text}")


async def main():
    # Устанавливаем вебхук при старте
    await set_webhook()

    # Запускаем FastAPI с вебхуком
    print("🚀 Бот запущен с Webhook!")
    print(f"📡 Webhook URL: {WEBHOOK_URL}")

    config = uvicorn.Config(app, host="0.0.0.0", port=8001, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
