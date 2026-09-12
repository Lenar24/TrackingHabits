"""
Тесты граничных случаев.
"""

import pytest
from datetime import date, timedelta

from backend.app.models import Habit


class TestEdgeCases:
    """Тесты граничных случаев."""

    def test_21_days_completion(self, client, auth_headers, db_session, test_user):
        """Автоматическое завершение после 21 дня."""
        # Создаём привычку с 20 днями
        habit = Habit(
            user_id=test_user.id,
            name="21 день",
            max_days=21,
            days_completed=20,
            last_completed=date.today() - timedelta(days=1),
            is_active=True,
        )
        db_session.add(habit)
        db_session.commit()

        # Выполняем 21-й день
        response = client.post(
            f"/api/v1/habits/{habit.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

        db_session.refresh(habit)
        assert habit.is_active is False
        assert habit.days_completed == 21

    def test_progress_after_gap(self, client, auth_headers, db_session, test_user):
        """Сброс прогресса после пропуска дня."""
        habit = Habit(
            user_id=test_user.id,
            name="С пропуском",
            max_days=21,
            days_completed=5,
            last_completed=date.today() - timedelta(days=3),
            is_active=True,
        )
        db_session.add(habit)
        db_session.commit()

        response = client.post(
            f"/api/v1/habits/{habit.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        # Прогресс сбрасывается +1
        assert data["habit"]["days_completed"] == 1

    def test_empty_habits_list(self, client, auth_headers):
        """Пустой список привычек."""
        response = client.get("/api/v1/habits/", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_many_habits(self, client, auth_headers, db_session, test_user):
        """Много привычек (пагинация)."""
        for i in range(150):
            habit = Habit(
                user_id=test_user.id,
                name=f"Привычка {i}",
                max_days=21,
            )
            db_session.add(habit)
        db_session.commit()

        response = client.get(
            "/api/v1/habits/?limit=100",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 100
