"""
Модуль является центральной точкой входа для всех обработчиков событий бота.
Он импортирует и экспортирует все функции-обработчики,
обеспечивая единый интерфейс для регистрации обработчиков в основном приложении бота.
Упрощает импорт и улучшает поддерживаемость кода.
"""

from .callback_handlers import handle_message_callback
from .command_handlers import handle_command
from .message_handlers import handle_bot_started, handle_message_created

__all__ = ["handle_bot_started", "handle_message_created", "handle_message_callback", "handle_command"]
