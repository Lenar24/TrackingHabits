"""
Модуль с валидаторами для данных бота.
"""

from typing import Optional

# Константы (синхронизированы с backend)
MAX_HABIT_NAME_LENGTH = 255
MAX_USERNAME_LENGTH = 100


def validate_habit_name(name: str) -> bool:
    """Проверка корректности названия привычки."""
    if not name or not name.strip():
        return False
    if len(name) > MAX_HABIT_NAME_LENGTH:
        return False
    return True


def validate_username(username: Optional[str]) -> bool:
    """Проверка корректности имени пользователя."""
    if username is None:
        return True
    if not username.strip():
        return False
    if len(username) > MAX_USERNAME_LENGTH:
        return False
    return True


def validate_chat_id(chat_id: int) -> bool:
    """Проверка корректности chat_id."""
    return chat_id is not None and chat_id > 0


def validate_user_id(user_id: int) -> bool:
    """Проверка корректности user_id."""
    return user_id is not None and user_id > 0


def sanitize_text(text: str) -> str:
    """Очистка текста от лишних пробелов."""
    if not text:
        return ""
    return " ".join(text.strip().split())
