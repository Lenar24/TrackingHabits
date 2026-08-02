import logging

from ..keyboards import create_main_keyboard
from ..services import HabitService
from ..utils import format_date

logger = logging.getLogger(__name__)


async def handle_bot_started(update_data: dict, bot, client):
    """Обработчик события bot_started"""
    try:
        chat_id = update_data.get("chat_id")
        user_id = update_data.get("user_id")
        logger.info(f"✅ Событие bot_started: chat_id={chat_id}")

        service = HabitService(client)
        await service.get_or_create_user(user_id, None, chat_id)

        await bot.send_message(
            chat_id=chat_id,
            text=(
                "🌟 Добро пожаловать в Трекер привычек!\n\n"
                "Я помогу вам:\n"
                "✅ Отслеживать ежедневные привычки\n"
                "📊 Видеть прогресс\n"
                "⏰ Напоминать о задачах\n\n"
                "Выберите действие в меню ниже:"
            ),
            attachments=create_main_keyboard(),
        )
    except Exception as e:
        logger.error(f"❌ Ошибка в bot_started: {e}")


async def handle_message_created(update_data: dict, bot, client):
    """Обработчик текстовых сообщений"""
    try:
        message_data = update_data.get("message")
        if not message_data:
            return

        chat_id = message_data.get("recipient", {}).get("chat_id")
        user_id = message_data.get("sender", {}).get("user_id")
        username = message_data.get("sender", {}).get("first_name")
        text = message_data.get("body", {}).get("text")

        logger.info(f"📩 Получено сообщение от {user_id} в чат {chat_id}")

        if not chat_id or not user_id:
            logger.warning("⚠️ Не удалось получить chat_id или user_id")
            return

        service = HabitService(client)
        await service.get_or_create_user(user_id, username, chat_id)

        if not text:
            return

        logger.info(f"💬 Текст: {text}")

        if text.lower() in ["начать", "/start", "start"]:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    "🌟 Добро пожаловать в Трекер привычек!\n\n"
                    "Я помогу вам:\n"
                    "✅ Отслеживать ежедневные привычки\n"
                    "📊 Видеть прогресс\n"
                    "⏰ Напоминать о задачах\n\n"
                    "Выберите действие в меню ниже:"
                ),
                attachments=create_main_keyboard(),
            )
            return

        if text.startswith("/"):
            return

        habit = await service.add_habit(user_id, text)
        if habit:
            habits_count = len(await service.get_habits(user_id))
            await bot.send_message(
                chat_id=chat_id,
                text=f"✅ **Привычка добавлена!**\n\n"
                f"📌 Название: **{text}**\n"
                f"👤 Владелец: {username or 'Пользователь'}\n"
                f"🎯 Цель: 21 дней\n"
                f"📊 Текущий прогресс: 0/21 дней\n\n"
                f"💡 Отмечайте выполнение каждый день через меню!",
                attachments=create_main_keyboard(),
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Не удалось добавить привычку. Возможно, она уже существует.",
                attachments=create_main_keyboard(),
            )
    except Exception as e:
        logger.error(f"❌ Ошибка в message_created: {e}")
