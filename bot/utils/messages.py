"""
Вспомогательные функции для отправки сообщений.
"""

import logging
from typing import Any, List, Dict

logger = logging.getLogger(__name__)


async def send_welcome_message(
    chat_id: int,
    bot: Any,
    keyboard: List[Dict[str, Any]]
) -> None:
    """Отправляет приветственное сообщение с клавиатурой."""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=(
                "🌟 Добро пожаловать в Трекер привычек!\n\n"
                "Я помогу Вам:\n"
                "✅ Отслеживать ежедневные привычки\n"
                "📊 Видеть прогресс\n"
                "⏰ Напоминать о задачах\n\n"
                "Выберите действие в меню ниже:"
            ),
            attachments=keyboard,
        )
        logger.info(f"✅ Приветствие отправлено в чат {chat_id}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки приветствия в чат {chat_id}: {e}")
        raise
