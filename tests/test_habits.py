"""
Тесты для привычек.
"""

import pytest
from datetime import date

from backend.app.models import Habit


class TestCreateHabit:
    """Тесты создания привычек."""

    def test_create_habit(self, client, auth_headers, test_user):
        """Создание привычки."""
        response = client.post(
            "/api/v1/habits/",
            headers=auth_headers,
            json={
                "name": "Новая привычка",
                "description": "Описание",
                "max_days": 21,
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Новая привычка"
        assert data["user_id"] == test_user.id
        assert data["days_completed"] == 0
        assert data["is_active"] is True

    def test_create_habit_duplicate(self, client, auth_headers, test_habit):
        """Создание дубликата привычки."""
        response = client.post(
            "/api/v1/habits/",
            headers=auth_headers,
            json={"name": test_habit.name}
        )
        assert response.status_code == 400
        assert "уже существует" in response.json()["detail"]

    def test_create_habit_empty_name(self, client, auth_headers):
        """Создание с пустым именем."""
        response = client.post(
            "/api/v1/habits/",
            headers=auth_headers,
            json={"name": ""}
        )
        assert response.status_code == 422

    def test_create_habit_unauthorized(self, client):
        """Создание без авторизации."""
        response = client.post(
            "/api/v1/habits/",
            json={"name": "Тест"}
        )
        assert response.status_code == 403


class TestGetHabits:
    """Тесты получения привычек."""

    def test_get_habits(self, client, auth_headers, test_habit):
        """Получение списка привычек."""
        response = client.get("/api/v1/habits/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_habits_active_only(self, client, auth_headers, test_habit):
        """Получение только активных."""
        response = client.get(
            "/api/v1/habits/?active_only=true",
            headers=auth_headers
        )
        assert response.status_code == 200

    def test_get_habit_by_id(self, client, auth_headers, test_habit):
        """Получение привычки по ID."""
        response = client.get(
            f"/api/v1/habits/{test_habit.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_habit.id

    def test_get_habit_not_found(self, client, auth_headers):
        """Получение несуществующей привычки."""
        response = client.get("/api/v1/habits/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_get_habit_other_user(self, client, auth_headers, db_session, test_user2):
        """Получение привычки другого пользователя."""
        other_habit = Habit(
            user_id=test_user2.id,
            name="Чужая привычка",
            max_days=21,
        )
        db_session.add(other_habit)
        db_session.commit()

        response = client.get(
            f"/api/v1/habits/{other_habit.id}",
            headers=auth_headers
        )
        assert response.status_code == 403


class TestUpdateHabit:
    """Тесты обновления привычек."""

    def test_update_habit(self, client, auth_headers, test_habit):
        """Обновление привычки."""
        response = client.put(
            f"/api/v1/habits/{test_habit.id}",
            headers=auth_headers,
            json={"name": "Обновлённое имя", "description": "Новое описание"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Обновлённое имя"
        assert data["description"] == "Новое описание"

    def test_update_habit_partial(self, client, auth_headers, test_habit):
        """Частичное обновление."""
        response = client.put(
            f"/api/v1/habits/{test_habit.id}",
            headers=auth_headers,
            json={"description": "Только описание"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_habit.name
        assert data["description"] == "Только описание"


class TestDeleteHabit:
    """Тесты удаления привычек."""

    def test_delete_habit(self, client, auth_headers, test_habit):
        """Удаление привычки."""
        response = client.delete(
            f"/api/v1/habits/{test_habit.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "deleted" in response.json()["message"].lower()

    def test_delete_habit_not_found(self, client, auth_headers):
        """Удаление несуществующей привычки."""
        response = client.delete("/api/v1/habits/99999", headers=auth_headers)
        assert response.status_code == 404


class TestCompleteHabit:
    """Тесты выполнения привычек."""

    def test_complete_habit(self, client, auth_headers, test_habit):
        """Выполнение привычки."""
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["habit"]["days_completed"] == 1
        assert data["habit"]["last_completed"] == str(date.today())

    def test_complete_habit_twice(self, client, auth_headers, test_habit):
        """Повторное выполнение в тот же день."""
        # Первое выполнение
        client.post(
            f"/api/v1/habits/{test_habit.id}/complete",
            headers=auth_headers
        )

        # Второе выполнение
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/complete",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert data["already_completed"] is True
        assert data["habit"]["days_completed"] == 1  # Не увеличилось

    def test_complete_habit_progress_1_21(self, client, auth_headers, test_habit):
        """Проверка прогресса после выполнения."""
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/complete",
            headers=auth_headers
        )
        data = response.json()
        assert data["progress"] == "1/21"


class TestSkipHabit:
    """Тесты пропуска привычек."""

    def test_skip_habit(self, client, auth_headers, test_habit):
        """Пропуск привычки."""
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/skip",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["habit"]["days_completed"] == 0
        assert data["habit"]["last_completed"] is None

    def test_skip_habit_after_complete(self, client, auth_headers, test_habit):
        """Пропуск после выполнения."""
        # Сначала выполняем
        client.post(
            f"/api/v1/habits/{test_habit.id}/complete",
            headers=auth_headers
        )

        # Пытаемся пропустить
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/skip",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Нельзя пропустить" in data["message"]


class TestCompleteEarly:
    """Тесты досрочного завершения."""

    def test_complete_early_not_enough_days(self, client, auth_headers, test_habit):
        """Досрочное завершение с < 7 днями."""
        response = client.post(
            f"/api/v1/habits/{test_habit.id}/complete-early",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "Минимум 7 дней" in data["message"]

    def test_complete_early_success(self, client, auth_headers, test_habit_7_days):
        """Досрочное завершение с 7 днями."""
        response = client.post(
            f"/api/v1/habits/{test_habit_7_days.id}/complete-early",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["habit"]["is_active"] is False
        assert data["habit"]["completed_early"] is True


class TestProgressAndStreak:
    """Тесты прогресса и стриков."""

    def test_get_progress(self, client, auth_headers, test_habit):
        """Получение прогресса."""
        response = client.get(
            f"/api/v1/habits/{test_habit.id}/progress",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "progress_percentage" in data
        assert "remaining_days" in data
        assert data["progress_percentage"] == 0.0

    def test_get_streak(self, client, auth_headers, test_habit):
        """Получение стрика."""
        response = client.get(
            f"/api/v1/habits/{test_habit.id}/streak",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "streak" in data
