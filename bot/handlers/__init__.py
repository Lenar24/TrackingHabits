"""
Модуль является центральной точкой входа для всех обработчиков событий бота.
"""

from .callback_handlers import (
    handle_complete_early,
    handle_habit_action,
    handle_mark_complete,
    handle_message_callback,
    handle_my_habits,
    handle_stats,
)
from .command_handlers import CommandContext, handle_command
from .message_handlers import handle_bot_started, handle_message_created

__all__ = [
    # Callback
    "handle_message_callback",
    "handle_my_habits",
    "handle_mark_complete",
    "handle_complete_early",
    "handle_stats",
    "handle_habit_action",
    # Command
    "handle_command",
    "CommandContext",
    # Message
    "handle_bot_started",
    "handle_message_created",
]
