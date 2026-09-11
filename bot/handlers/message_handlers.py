"""
Модуль отвечает за обработку основных событий бота.
"""

import logging
from typing import Any, Dict

import httpx

from ..keyboards import create_main_keyboard
from ..services import HabitService
from ..services.auth_service import AuthService
from ..database import TokenDB
from ..utils.messages import send_welcome_message

logger = logging.getLogger(__name__)


async def handle_bot_started(
    update_data: Dict[str, Any],
    bot,
    client,
    auth_service: AuthService,
    token_db: TokenDB,
) -> None:
    """Обработка события запуска бота (при старте или перезапуске)."""
    try:
        chat_id = update_data.get("chat_id")
        user_id = update_data.get("user_id")
        logger.info(f"✅ Событие bot_started: chat_id={chat_id}")

        if user_id is None or chat_id is None:
            logger.warning("⚠️ user_id или chat_id отсутствуют")
            return

        service = HabitService(client, auth_service, token_db)
        await service.get_or_create_user(int(user_id), None, int(chat_id))

        await send_welcome_message(chat_id, bot, create_main_keyboard())
    except (httpx.HTTPError, ValueError, KeyError) as e:
        logger.error(f"❌ Ошибка в bot_started: {e}")


async def handle_message_created(
    update_data: Dict[str, Any],
    bot,
    client,
    auth_service: AuthService,
    token_db: TokenDB,
) -> None:
    """Обработка входящих текстовых сообщений от пользователя."""
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

        if not text:
            return

        logger.info(f"💬 Текст: {text}")

        service = HabitService(client, auth_service, token_db)
        await service.get_or_create_user(int(user_id), username if username else None, int(chat_id))

        if text.lower() in ["начать", "/start", "start"]:
            await send_welcome_message(chat_id, bot, create_main_keyboard())
            return

        if text.startswith("/"):
            return

        habit = await service.add_habit(int(user_id), text, chat_id=int(chat_id))
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
        logger.error(f"❌ Ошибка в message_created: {e}")
