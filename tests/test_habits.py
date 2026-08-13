"""
Тесты для эндпоинтов привычек.
Проверяет все операции CRUD и сценарии работы с привычками.
"""

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time


@pytest.mark.unit
class TestHabitsAPI:
    """Тесты API привычек"""

    def test_create_habit(self, client: TestClient):
        """Тест создания привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})

        response = client.post(
            "/habits/", json={"user_id": 12345, "name": "Читать книги", "description": "Читать 30 минут в день"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Читать книги"
        assert data["user_id"] == 12345
        assert data["is_active"] is True
        assert not data["days_completed"]
        assert data["max_days"] == 21

    def test_get_habits(self, client: TestClient):
        """Тест получения списка привычек"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        client.post("/habits/", json={"user_id": 12345, "name": "Привычка 1"})
        client.post("/habits/", json={"user_id": 12345, "name": "Привычка 2"})

        response = client.get("/habits/12345")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @freeze_time("2026-01-01")
    def test_get_habits_active_only(self, client: TestClient):
        """Тест получения только активных привычек"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})

        # Создаём привычку
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Завершённая"})
        habit_id = create_response.json()["id"]

        # Отмечаем 21 день (используем freeze_time для имитации дней)
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Создаём активную привычку
        client.post("/habits/", json={"user_id": 12345, "name": "Активная"})

        # Получаем только активные
        response = client.get("/habits/12345")
        assert response.status_code == 200
        data = response.json()
        # Должна быть только активная привычка
        assert len(data) == 1
        assert data[0]["name"] == "Активная"
        assert data[0]["is_active"] is True

    def test_get_habit_by_id(self, client: TestClient):
        """Тест получения привычки по ID"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Тестовая привычка"})
        habit_id = create_response.json()["id"]

        response = client.get(f"/habits/item/{habit_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Тестовая привычка"
        assert data["id"] == habit_id

    def test_get_habit_by_id_not_found(self, client: TestClient):
        """Тест получения несуществующей привычки"""
        response = client.get("/habits/item/99999")
        assert response.status_code == 404

    @freeze_time("2026-01-01")
    def test_complete_habit(self, client: TestClient):
        """Тест отметки выполнения привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Выполняемая привычка"})
        habit_id = create_response.json()["id"]

        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["days_completed"] == 1
        assert data["last_completed"] == "2026-01-01"
        assert data["is_active"] is True

    @freeze_time("2026-01-01")
    def test_complete_habit_already_completed_today(self, client: TestClient):
        """Тест повторной отметки в тот же день"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Привычка"})
        habit_id = create_response.json()["id"]

        client.post(f"/habits/{habit_id}/complete")
        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["days_completed"] == 1

    @freeze_time("2026-01-01")
    def test_habit_progress_after_multiple_completions(self, client: TestClient):
        """Тест прогресса после нескольких выполнений в разные дни"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Прогрессивная"})
        habit_id = create_response.json()["id"]

        # Отмечаем 5 дней с разными датами
        for day in range(5):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                response = client.post(f"/habits/{habit_id}/complete")
                assert response.status_code == 200
                data = response.json()
                assert data["days_completed"] == day + 1

        # Проверяем финальный прогресс
        response = client.get(f"/habits/item/{habit_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["days_completed"] == 5

    @freeze_time("2026-01-01")
    def test_habit_auto_complete_at_21_days(self, client: TestClient):
        """Тест автоматического завершения после 21 дня"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "21-дневная"})
        habit_id = create_response.json()["id"]

        # Отмечаем 21 день с разными датами
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                response = client.post(f"/habits/{habit_id}/complete")
                assert response.status_code == 200
                data = response.json()
                if day == 20:  # 21-й день
                    assert data["is_active"] is False
                    assert data["days_completed"] == 21
                else:
                    assert data["is_active"] is True

    @freeze_time("2026-01-01")
    def test_habit_skip_resets_progress(self, client: TestClient):
        """Тест сброса прогресса при пропуске"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Сбрасываемая"})
        habit_id = create_response.json()["id"]

        # Отмечаем 5 дней
        for day in range(5):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Проверяем прогресс
        response = client.get(f"/habits/item/{habit_id}")
        assert response.json()["days_completed"] == 5

        # Пропускаем
        with freeze_time("2026-01-06"):
            client.post(f"/habits/{habit_id}/skip")

        # Проверяем, что прогресс сброшен
        response = client.get(f"/habits/item/{habit_id}")
        assert not response.json()["days_completed"]

    def test_delete_habit(self, client: TestClient):
        """Тест удаления привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Удаляемая"})
        habit_id = create_response.json()["id"]

        response = client.delete(f"/habits/{habit_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Habit deleted"}

        get_response = client.get(f"/habits/item/{habit_id}")
        assert get_response.status_code == 404

    def test_delete_habit_not_found(self, client: TestClient):
        """Тест удаления несуществующей привычки"""
        response = client.delete("/habits/99999")
        assert response.status_code == 404

    @freeze_time("2026-01-01")
    def test_update_habit(self, client: TestClient):
        """Тест обновления привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Старое название"})
        habit_id = create_response.json()["id"]

        response = client.put(
            f"/habits/{habit_id}", json={"name": "Новое название", "description": "Новое описание", "is_active": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Новое название"
        assert data["description"] == "Новое описание"
        assert data["is_active"] is False

    def test_update_habit_not_found(self, client: TestClient):
        """Тест обновления несуществующей привычки"""
        response = client.put("/habits/99999", json={"name": "Новое название"})
        assert response.status_code == 404

    def test_complete_habit_early(self, client: TestClient):
        """Тест досрочного завершения"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Досрочная"})
        habit_id = create_response.json()["id"]

        response = client.post(f"/habits/{habit_id}/complete-early")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        assert data["days_completed"] == 21
        assert data["completed_early"] is True

    def test_habit_response_structure(self, client: TestClient):
        """Тест структуры ответа"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Структурная"})
        habit_id = create_response.json()["id"]

        response = client.get(f"/habits/item/{habit_id}")
        assert response.status_code == 200
        data = response.json()

        expected_fields = [
            "id",
            "user_id",
            "name",
            "description",
            "created_at",
            "is_active",
            "days_completed",
            "max_days",
            "last_completed",
            "completed_at",
            "completed_early",
        ]
        for field in expected_fields:
            assert field in data


@pytest.mark.slow
class TestHabitsSlow:  # pylint: disable=too-few-public-methods
    """Медленные тесты"""

    @freeze_time("2026-01-01")
    def test_complete_habit_21_days_slow(self, client: TestClient):
        """Тест полного цикла 21 день"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Долгая"})
        habit_id = create_response.json()["id"]

        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                response = client.post(f"/habits/{habit_id}/complete")
                assert response.status_code == 200
                data = response.json()
                assert data["days_completed"] == day + 1


@pytest.mark.integration
class TestHabitsIntegration:
    """Интеграционные тесты"""

    @freeze_time("2026-01-01")
    def test_habit_with_logs_integration(self, client: TestClient):
        """Интеграционный тест: привычка с логами"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Привычка с логами"})
        habit_id = create_response.json()["id"]

        for day in range(7):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 1
        assert stats[0]["name"] == "Привычка с логами"
        assert stats[0]["days_completed"] == 7
        assert stats[0]["total_logs"] >= 7

    @freeze_time("2026-01-01")
    def test_habit_complete_early_with_stats(self, client: TestClient):
        """Тест досрочного завершения со статистикой"""
        client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Досрочная с логами"})
        habit_id = create_response.json()["id"]

        for day in range(5):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        client.post(f"/habits/{habit_id}/complete-early")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 1
        assert stats[0]["name"] == "Досрочная с логами"
        assert stats[0]["days_completed"] == 21
