"""
Тесты планировщика задач.
"""

from unittest.mock import MagicMock, patch
import pytest

from backend.app.scheduler import (
    send_daily_reminders,
    send_reminder_to_user,
    start_scheduler,
    check_21_days_job
)


class TestScheduler:
    """Тесты планировщика"""

    @pytest.mark.asyncio
    async def test_send_daily_reminders(self):
        """Тест отправки ежедневных напоминаний"""
        with patch("backend.app.scheduler.get_users_with_habits") as mock_users:
            mock_users.return_value = [
                {"user_id": 123, "chat_id": 456, "habits": [{"name": "Test"}]}
            ]

            with patch("backend.app.scheduler.send_reminder_to_user") as mock_send:
                await send_daily_reminders()
                mock_send.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_reminder_to_user(self):
        """Тест отправки напоминания пользователю"""
        habits = [{"name": "Test Habit", "is_active": True, "days_completed": 5, "max_days": 21}]

        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value.status_code = 200
            await send_reminder_to_user(123, habits, 456)
            assert mock_post.called

    def test_scheduler_start(self):
        """Тест запуска планировщика"""
        scheduler = start_scheduler()
        assert scheduler is not None
        assert scheduler.running
        scheduler.shutdown()

    def test_check_21_days_job(self):
        """Тест задания проверки 21 дня"""
        with patch("backend.app.scheduler.HabitService.check_21_days") as mock_check:
            with patch("backend.app.scheduler.SessionLocal"):
                check_21_days_job()
                mock_check.assert_called_once()

    def test_check_21_days_job_with_session(self):
        """Тест задания проверки 21 дня с сессией"""
        mock_session = MagicMock()

        with patch("backend.app.scheduler.SessionLocal", return_value=mock_session):
            # Мокаем статический метод
            with patch("backend.app.scheduler.HabitService.check_21_days") as mock_check:
                check_21_days_job()
                mock_check.assert_called_once_with(mock_session)
                mock_session.close.assert_called_once()
