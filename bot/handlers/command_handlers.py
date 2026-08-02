import logging

from ..keyboards import create_main_keyboard
from ..services import HabitService

logger = logging.getLogger(__name__)


async def handle_command(command: str, chat_id: int, user_id: int, username: str, bot, client):
    """Обработчик команд (для постоянного меню)"""
    service = HabitService(client)
    await service.get_or_create_user(user_id, username, chat_id)

    if command == "start":
        await bot.send_message(
            chat_id=chat_id,
            text="🌟 Добро пожаловать в Трекер привычек!\n\nВыберите действие в меню ниже:",
            attachments=create_main_keyboard(),
        )

    elif command == "habits":
        habits = await service.get_habits(user_id)
        from ..utils import format_habit_list

        text = format_habit_list(habits, username)
        await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())

    elif command == "add":
        await bot.send_message(
            chat_id=chat_id,
            text="✏️ **Введите название новой привычки:**\n\nНапример: «Читать 30 минут» или «Заниматься спортом»",
            attachments=create_main_keyboard(),
        )

    elif command == "complete":
        from .callback_handlers import handle_mark_complete

        await handle_mark_complete(chat_id, user_id, bot, service)

    elif command == "finish":
        from .callback_handlers import handle_complete_early

        await handle_complete_early(chat_id, user_id, bot, service)

    elif command == "stats":
        from ..utils import format_statistics

        stats = await service.get_stats(user_id)
        text = format_statistics(stats, username)
        await bot.send_message(chat_id=chat_id, text=text, attachments=create_main_keyboard())
