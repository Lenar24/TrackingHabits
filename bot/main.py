import os
import asyncio
import logging
from dotenv import load_dotenv

from maxapi import Bot, Dispatcher
from maxapi.types import BotStarted, MessageCreated, Command, MessageCallback
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

bot = Bot(token=os.getenv("MAX_BOT_TOKEN"))
dp = Dispatcher()

# Словарь для имитации хранения привычек пользователей
user_habits = {}


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
    """
    Обработчик нажатий на inline-кнопки (событие message_callback)
    """
    logger.info(f"🔘 Получен callback: {event}")

    # Получаем chat_id
    chat_id = None
    if hasattr(event, 'chat_id'):
        chat_id = event.chat_id
    elif hasattr(event, 'chat') and hasattr(event.chat, 'chat_id'):
        chat_id = event.chat.chat_id
    elif hasattr(event.message, 'recipient') and hasattr(event.message.recipient, 'chat_id'):
        chat_id = event.message.recipient.chat_id

    if not chat_id:
        logger.error("❌ Не удалось получить chat_id в callback")
        return

    # Получаем user_id
    user_id = None
    if hasattr(event, 'user_id'):
        user_id = event.user_id
    elif hasattr(event, 'from_user') and hasattr(event.from_user, 'user_id'):
        user_id = event.from_user.user_id
    elif hasattr(event.message, 'sender') and hasattr(event.message.sender, 'user_id'):
        user_id = event.message.sender.user_id

    if not user_id:
        logger.error("❌ Не удалось получить user_id в callback")
        return

    # --- ПРАВИЛЬНОЕ ПОЛУЧЕНИЕ PAYLOAD ---
    # В MAX API payload лежит в event.callback.payload
    payload = None
    if hasattr(event, 'callback') and hasattr(event.callback, 'payload'):
        payload = event.callback.payload
        logger.info(f"🔘 Payload из event.callback.payload: {payload}")
    elif hasattr(event, 'payload'):
        payload = event.payload
        logger.info(f"🔘 Payload из event.payload: {payload}")
    elif hasattr(event.message, 'payload'):
        payload = event.message.payload
        logger.info(f"🔘 Payload из event.message.payload: {payload}")

    if not payload:
        logger.error("❌ Не удалось получить payload в callback")
        return

    # Обработка действий
    if payload == "my_habits":
        habits = user_habits.get(user_id, [])
        if not habits:
            await bot.send_message(
                chat_id=chat_id,
                text="📋 У вас пока нет привычек. Нажмите «➕ Добавить привычку»."
            )
        else:
            habits_text = "📋 Ваши привычки:\n\n"
            for i, habit in enumerate(habits, 1):
                habits_text += f"{i}. {habit}\n"
            await bot.send_message(
                chat_id=chat_id,
                text=habits_text
            )

    elif payload == "add_habit":
        await bot.send_message(
            chat_id=chat_id,
            text="✏️ Введите название новой привычки:"
        )

    elif payload and payload.startswith("habit_"):
        action = payload.split("_")[1]
        if action == "done":
            await bot.send_message(
                chat_id=chat_id,
                text="✅ Привычка отмечена как выполненная!"
            )
        elif action == "delete":
            await bot.send_message(
                chat_id=chat_id,
                text="🗑️ Привычка удалена"
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
        logger.info(f"💬 Текст из body.text: {text}")
    elif hasattr(event.message, 'text'):
        text = event.message.text
        logger.info(f"💬 Текст из message.text: {text}")

    # Обработка команды "Начать" или "start"
    if text:
        logger.info(f"💬 Обработка текста: '{text}'")
        if text.lower() in ["начать", "/start", "start"]:
            logger.info(f"🔄 Отправка приветствия для chat_id={chat_id}")
            await send_welcome(chat_id)
            return
    else:
        logger.warning("⚠️ Текст не найден в сообщении")
        return

    # --- Обработка обычных текстовых сообщений (добавление привычек) ---
    if not text or text.startswith('/'):
        return

    # Простая логика: считаем любой текст новой привычкой
    if user_id not in user_habits:
        user_habits[user_id] = []
    user_habits[user_id].append(text)

    await bot.send_message(
        chat_id=chat_id,
        text=f"✅ Привычка «{text}» добавлена!\n"
             f"📋 Всего привычек: {len(user_habits[user_id])}"
    )


async def main():
    print("🚀 Бот запущен и готов к работе!")
    print("📝 Логи будут отображаться ниже...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())