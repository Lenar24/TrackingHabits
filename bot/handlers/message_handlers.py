"""
Модуль отвечает за обработку основных событий бота: запуск бота (bot_started)
и получение текстовых сообщений (message_created).
Обрабатывает регистрацию пользователей, создание привычек через текстовый ввод
и приветствие новых пользователей.
"""

import logging

import httpx

from ..keyboards import create_main_keyboard
from ..services import HabitService
from ..utils.messages import send_welcome_message

logger = logging.getLogger(__name__)


async def handle_bot_started(update_data: dict, bot, client):
    """Обработка события запуска бота (при старте или перезапуске)."""
    try:
        chat_id = update_data.get("chat_id")
        user_id = update_data.get("user_id")
        logger.info("✅ Событие bot_started: chat_id=%s", chat_id)

        service = HabitService(client)
        await service.get_or_create_user(user_id, None, chat_id)

        await send_welcome_message(chat_id, bot, create_main_keyboard())
    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.error("❌ Ошибка в bot_started: %s", e)


async def handle_message_created(update_data: dict, bot, client):
    """Обработка входящих текстовых сообщений от пользователя."""
    try:
        message_data = update_data.get("message")
        if not message_data:
            return

        chat_id = message_data.get("recipient", {}).get("chat_id")
        user_id = message_data.get("sender", {}).get("user_id")
        username = message_data.get("sender", {}).get("first_name")
        text = message_data.get("body", {}).get("text")

        logger.info("📩 Получено сообщение от %s в чат %s", user_id, chat_id)

        if not chat_id or not user_id:
            logger.warning("⚠️ Не удалось получить chat_id или user_id")
            return

        service = HabitService(client)
        await service.get_or_create_user(user_id, username, chat_id)

        if not text:
            return

        logger.info("💬 Текст: %s", text)

        if text.lower() in ["начать", "/start", "start"]:
            await send_welcome_message(chat_id, bot, create_main_keyboard())
            return

        if text.startswith("/"):
            return

        habit = await service.add_habit(user_id, text)
        if habit:
            await bot.send_message(
                chat_id=chat_id,
                text=(
                    f"✅ **Привычка добавлена!**\n\n"
                    f"📌 Название: **{text}**\n"
                    f"👤 Владелец: {username or 'Пользователь'}\n"
                    f"🎯 Цель: 21 дней\n"
                    f"📊 Текущий прогресс: 0/21 дней\n\n"
                    f"💡 Отмечайте выполнение каждый день через меню!"
                ),
                attachments=create_main_keyboard(),
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text="❌ Не удалось добавить привычку. Возможно, она уже существует.",
                attachments=create_main_keyboard(),
            )
    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.error("❌ Ошибка в message_created: %s", e)
