"""
Тесты валидации данных.
"""

import pytest

from backend.app.utils.validators import (
    validate_habit_name,
    validate_username,
    validate_chat_id,
    validate_max_days,
)


class TestValidators:
    """Тесты валидаторов."""

    def test_validate_habit_name_valid(self):
        """Валидное имя привычки."""
        assert validate_habit_name("Зарядка") is True
        assert validate_habit_name("A" * 255) is True

    def test_validate_habit_name_invalid(self):
        """Невалидное имя привычки."""
        assert validate_habit_name("") is False
        assert validate_habit_name("   ") is False
        assert validate_habit_name("A" * 256) is False

    def test_validate_username_valid(self):
        """Валидное имя пользователя."""
        assert validate_username("user") is True
        assert validate_username(None) is True

    def test_validate_username_invalid(self):
        """Невалидное имя пользователя."""
        assert validate_username("") is False
        assert validate_username("A" * 101) is False

    def test_validate_chat_id(self):
        """Валидация chat_id."""
        assert validate_chat_id(123) is True
        assert validate_chat_id(0) is False
        assert validate_chat_id(-1) is False

    def test_validate_max_days(self):
        """Валидация max_days."""
        assert validate_max_days(21) is True
        assert validate_max_days(1) is True
        assert validate_max_days(365) is True
        assert validate_max_days(0) is False
        assert validate_max_days(366) is False
