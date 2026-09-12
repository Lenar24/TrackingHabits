"""
Модуль с валидаторами для данных.
"""

import re
from typing import Optional


def validate_habit_name(name: str) -> bool:
    """
    Валидация названия привычки.

    Args:
        name: Название привычки

    Returns:
        bool: True если валидно
    """
    if not name or not name.strip():
        return False
    if len(name) > 255:
        return False
    return True


def validate_username(username: Optional[str]) -> bool:
    """
    Валидация имени пользователя.

    Args:
        username: Имя пользователя

    Returns:
        bool: True если валидно
    """
    if username is None:
        return True
    if not username.strip():
        return False
    if len(username) > 100:
        return False
    if not re.match(r'^[\w\-_.@]+$', username):
        return False
    return True


def validate_chat_id(chat_id: int) -> bool:
    """
    Валидация chat_id.

    Args:
        chat_id: ID чата

    Returns:
        bool: True если валидно
    """
    return chat_id is not None and chat_id > 0


def validate_max_days(days: int) -> bool:
    """
    Валидация количества дней.

    Args:
        days: Количество дней

    Returns:
        bool: True если валидно
    """
    return 1 <= days <= 365
