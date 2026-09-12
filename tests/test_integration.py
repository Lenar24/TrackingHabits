"""
Интеграционные тесты полного флоу.
"""

import pytest
from datetime import date


class TestFullFlow:
    """Тесты полного флоу."""

    def test_full_habit_lifecycle(self, client, db_session):
        """Полный жизненный цикл привычки."""
        # 1. Логин
        login_response = client.post(
            "/api/v1/auth/login",
            json={"max_user_id": 77777, "chat_id": 88888}
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Создание привычки
        create_response = client.post(
            "/api/v1/habits/",
            headers=headers,
            json={"name": "Тестовая привычка", "max_days": 21}
        )
        assert create_response.status_code == 201
        habit_id = create_response.json()["id"]

        # 3. Получение привычки
        get_response = client.get(
            f"/api/v1/habits/{habit_id}",
            headers=headers
        )
        assert get_response.status_code == 200

        # 4. Выполнение
        complete_response = client.post(
            f"/api/v1/habits/{habit_id}/complete",
            headers=headers
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["habit"]["days_completed"] == 1

        # 5. Повторное выполнение
        complete2_response = client.post(
            f"/api/v1/habits/{habit_id}/complete",
            headers=headers
        )
        assert complete2_response.json()["success"] is False

        # 6. Прогресс
        progress_response = client.get(
            f"/api/v1/habits/{habit_id}/progress",
            headers=headers
        )
        assert progress_response.status_code == 200

        # 7. Статистика
        stats_response = client.get(
            "/api/v1/stats/overall",
            headers=headers
        )
        assert stats_response.status_code == 200
        assert stats_response.json()["total_habits"] == 1

        # 8. Удаление
        delete_response = client.delete(
            f"/api/v1/habits/{habit_id}",
            headers=headers
        )
        assert delete_response.status_code == 200

        # 9. Проверка удаления
        get_after_delete = client.get(
            f"/api/v1/habits/{habit_id}",
            headers=headers
        )
        assert get_after_delete.status_code == 404
