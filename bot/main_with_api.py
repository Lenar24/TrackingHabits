import os
import asyncio
import logging
from dotenv import load_dotenv
import httpx

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, MessageCreated, Command, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Конфигурация
MAX_BOT_TOKEN = os.getenv("MAX_BOT_TOKEN")
# API_URL = "http://backend:8000"  # Внутри Docker-сети
API_URL = "http://localhost:8000"  # Для доступа с хоста

bot = Bot(token=MAX_BOT_TOKEN)
dp = Dispatcher()

# HTTP-клиент для запросов к API
client = httpx.AsyncClient(timeout=30.0)


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


async def get_or_create_user(user_id: int, username: str = None):
    """Получить или создать пользователя в БД"""
    # Проверяем, есть ли пользователь
    response = await client.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        return response.json()

    # Создаём нового пользователя
    response = await client.post(
        f"{API_URL}/users/",
        json={"user_id": user_id, "username": username}
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


@dp.bot_started()
async def bot_started(event: BotStarted):
    """Приветственное сообщение при запуске бота"""
    logger.info(f"✅ Событие bot_started: chat_id={event.chat_id}")
    await send_welcome(event.chat_id)


@dp.message_created(Command('start'))
async def start_command(event: MessageCreated):
    """Обработка команды /start"""
    chat_id = event.message.recipient.chat_id if hasattr(event.message, 'recipient') else None
    logger.info(f"✅ Команда /start от chat_id={chat_id}")
    if chat_id:
        await send_welcome(chat_id)


@dp.message_callback()
async def handle_callback(event: MessageCallback):
    """Обработчик нажатий на inline-кнопки"""
    logger.info(f"🔘 Получен callback: {event}")

    # Получаем chat_id
    chat_id = None
    if hasattr(event, 'chat_id'):
        chat_id = event.chat_id
    elif hasattr(event, 'chat') and hasattr(event.chat, 'chat_id'):
        chat_id = event.chat.chat_id

    if not chat_id:
        logger.error("❌ Не удалось получить chat_id в callback")
        return

    # Получаем user_id
    user_id = None
    if hasattr(event, 'from_user') and hasattr(event.from_user, 'user_id'):
        user_id = event.from_user.user_id

    if not user_id:
        logger.error("❌ Не удалось получить user_id в callback")
        return

    # Получаем payload
    payload = None
    if hasattr(event, 'callback') and hasattr(event.callback, 'payload'):
        payload = event.callback.payload

    if not payload:
        logger.error("❌ Не удалось получить payload в callback")
        return

    logger.info(f"🔘 Payload: {payload}")

    # Создаём или получаем пользователя
    username = event.from_user.first_name if hasattr(event, 'from_user') else None
    await get_or_create_user(user_id, username)

    # Обработка действий
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


@dp.message_created()
async def handle_all_messages(event: MessageCreated):
    """Универсальный обработчик для текстовых сообщений"""
    logger.info(f"📩 Получено сообщение: {event.message}")

    # Получаем chat_id
    chat_id = None
    if hasattr(event.message, 'recipient') and hasattr(event.message.recipient, 'chat_id'):
        chat_id = event.message.recipient.chat_id
    elif hasattr(event, 'chat_id'):
        chat_id = event.chat_id

    if not chat_id:
        logger.error("❌ Не удалось получить chat_id")
        return

    # Получаем user_id
    user_id = None
    if hasattr(event.message, 'sender') and hasattr(event.message.sender, 'user_id'):
        user_id = event.message.sender.user_id
    elif hasattr(event, 'user_id'):
        user_id = event.user_id

    if not user_id:
        logger.error("❌ Не удалось получить user_id")
        return

    # Получаем текст
    text = None
    if hasattr(event.message, 'body') and hasattr(event.message.body, 'text'):
        text = event.message.body.text

    # Обработка команды "Начать" или "start"
    if text:
        if text.lower() in ["начать", "/start", "start"]:
            await send_welcome(chat_id)
            return
    else:
        logger.warning("⚠️ Текст не найден в сообщении")
        return

    # --- Обработка обычных текстовых сообщений (добавление привычек) ---
    if not text or text.startswith('/'):
        return

    # Создаём пользователя, если его нет
    username = event.message.sender.first_name if hasattr(event.message, 'sender') else None
    await get_or_create_user(user_id, username)

    # Добавляем привычку через API
    habit = await add_user_habit(user_id, text)
    if habit:
        await bot.send_message(
            chat_id=chat_id,
            text=f"✅ Привычка «{text}» добавлена!\n"
                 f"📋 Всего привычек: {len(await get_user_habits(user_id))}"
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="❌ Не удалось добавить привычку. Попробуйте позже."
        )


async def main():
    print("🚀 Бот запущен и готов к работе!")
    print("📝 Логи будут отображаться ниже...")
    try:
        await dp.start_polling(bot)
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
