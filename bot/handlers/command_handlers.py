"""
Модуль отвечает за обработку текстовых команд от пользователя в MAX боте.
Обрабатывает команды из постоянного меню (start, habits, add, complete,
finish, stats) и перенаправляет выполнение на соответствующие обработчики.
"""

import logging
from dataclasses import dataclass
from typing import Any

from ..keyboards import create_main_keyboard
from ..services import HabitService
from ..utils import format_habit_list, format_statistics
from .callback_handlers import handle_complete_early, handle_mark_complete

logger = logging.getLogger(__name__)


@dataclass
class CommandContext:
    """Контекст команды."""

    command: str
    chat_id: int
    user_id: int
    username: str
    bot: Any
    client: Any


async def handle_command(ctx: CommandContext):
    """Основной обработчик текстовых команд от пользователя."""
    service = HabitService(ctx.client)
    await service.get_or_create_user(ctx.user_id, ctx.username, ctx.chat_id)

    if ctx.command == "start":
        await ctx.bot.send_message(
            chat_id=ctx.chat_id,
            text="🌟 Добро пожаловать в Трекер привычек!\n\nВыберите действие в меню ниже:",
            attachments=create_main_keyboard(),
        )

    elif ctx.command == "habits":
        habits = await service.get_habits(ctx.user_id)
        text = format_habit_list(habits, ctx.username)
        await ctx.bot.send_message(chat_id=ctx.chat_id, text=text, attachments=create_main_keyboard())

    elif ctx.command == "add":
        await ctx.bot.send_message(
            chat_id=ctx.chat_id,
            text=("✏️ **Введите название новой привычки:**\n\n" "Например: «Читать 30 минут» или «Заниматься спортом»"),
            attachments=create_main_keyboard(),
        )

    elif ctx.command == "complete":
        await handle_mark_complete(ctx.chat_id, ctx.user_id, ctx.bot, service)

    elif ctx.command == "finish":
        await handle_complete_early(ctx.chat_id, ctx.user_id, ctx.bot, service)

    elif ctx.command == "stats":
        stats = await service.get_stats(ctx.user_id)
        text = format_statistics(stats, ctx.username)
        await ctx.bot.send_message(chat_id=ctx.chat_id, text=text, attachments=create_main_keyboard())
