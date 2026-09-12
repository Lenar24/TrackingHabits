"""
Тесты для бота.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from bot.utils.formatters import format_habit_list, format_statistics
from bot.utils.validators import validate_habit_name


class TestFormatters:
    """Тесты форматирования."""

    def test_format_habit_list_empty(self):
        """Пустой список привычек."""
        result = format_habit_list([])
        assert "нет привычек" in result

    def test_format_habit_list(self):
        """Список привычек."""
        habits = [
            {"name": "Тест", "days_completed": 5, "max_days": 21, "is_active": True},
        ]
        result = format_habit_list(habits)
        assert "Тест" in result
        assert "5/21" in result

    def test_format_statistics_dict(self):
        """Статистика (dict)."""
        stats = {
            "total_habits": 6,
            "active_habits": 5,
            "completed_habits": 1,
            "total_days_completed": 30,
            "best_overall_streak": 7,
            "completion_rate": 16.7,
        }
        result = format_statistics(stats)
        assert "Всего привычек:** 6" in result
        assert "Активных:** 5" in result
        assert "Завершено:** 1" in result
        assert "Всего выполнено дней:** 30" in result
        assert "Лучшая серия:** 7" in result
        assert "Эффективность:** 16.7%" in result

    def test_format_statistics_empty(self):
        """Пустая статистика."""
        result = format_statistics({})
        assert "нет привычек" in result


class TestValidators:
    """Тесты валидаторов бота."""

    def test_validate_habit_name(self):
        """Валидация имени привычки."""
        assert validate_habit_name("Тест") is True
        assert validate_habit_name("") is False
        assert validate_habit_name("   ") is False
        assert validate_habit_name("A" * 256) is False
