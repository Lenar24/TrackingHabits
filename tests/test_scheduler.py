"""
Тесты для планировщика.
"""

from unittest.mock import MagicMock, patch

from backend.app.scheduler import (
    _format_habits_message,
    get_internal_token,
    check_21_days_job,
)


class TestScheduler:
    """Тесты планировщика."""

    def test_format_habits_message_empty(self):
        """Пустой список привычек."""
        result = _format_habits_message([])
        assert "нет активных привычек" in result

    def test_format_habits_message(self):
        """Форматирование привычек."""
        habits = [
            {"name": "Тест", "days_completed": 5, "max_days": 21, "is_active": True},
        ]
        result = _format_habits_message(habits)
        assert "Тест" in result
        assert "5/21" in result

    def test_get_internal_token(self):
        """Получение системного токена."""
        token = get_internal_token()
        assert token is not None
        assert isinstance(token, str)

    @patch("backend.app.scheduler.SessionLocal")
    def test_check_21_days_job(self, mock_session):
        """Проверка 21 дня."""
        mock_db = MagicMock()
        mock_session.return_value = mock_db

        result = check_21_days_job()
        assert "updated" in result
        assert "completed" in result
