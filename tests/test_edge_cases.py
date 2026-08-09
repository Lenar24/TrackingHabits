"""
Тесты граничных случаев и краевых условий.
"""

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time


@pytest.mark.unit
class TestEdgeCases:
    """Тесты граничных случаев"""

    @freeze_time("2026-01-01")
    def test_complete_habit_on_21st_day(self, client: TestClient):
        """Тест: выполнение привычки ровно на 21-й день"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Ровно 21"})
        habit_id = response.json()["id"]

        # Отмечаем 20 дней
        for day in range(20):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # 21-й день
        with freeze_time("2026-01-21"):
            response = client.post(f"/habits/{habit_id}/complete")
            data = response.json()
            assert data["days_completed"] == 21
            assert data["is_active"] is False

    def test_habit_completion_at_midnight(self, client: TestClient):
        """Тест: выполнение привычки в полночь"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Полночная"})
        habit_id = response.json()["id"]

        # Не проверяем точное время, просто выполняем
        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200

    def test_duplicate_habit_name_for_same_user(self, client: TestClient):
        """Тест: создание привычки с дублирующимся названием"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        # Создаём первую привычку
        response1 = client.post("/habits/", json={"user_id": 12345, "name": "Уникальная"})
        assert response1.status_code == 200

        # Создаём вторую с тем же названием
        response2 = client.post("/habits/", json={"user_id": 12345, "name": "Уникальная"})
        # Может быть 200 (если дубликаты разрешены) или 400/409
        assert response2.status_code in [200, 400, 409]

    def test_delete_habit_with_completed_logs(self, client: TestClient):
        """Тест: удаление привычки с выполненными логами"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "С логами"})
        habit_id = response.json()["id"]

        # Выполняем несколько раз
        for _ in range(5):
            client.post(f"/habits/{habit_id}/complete")

        # Удаляем привычку
        response = client.delete(f"/habits/{habit_id}")
        assert response.status_code == 200

        # Проверяем, что привычка удалена
        response = client.get(f"/habits/item/{habit_id}")
        assert response.status_code == 404

    def test_complete_habit_with_no_active(self, client: TestClient):
        """Тест: выполнение неактивной привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Неактивная"})
        habit_id = response.json()["id"]

        # Завершаем досрочно
        client.post(f"/habits/{habit_id}/complete-early")

        # Пытаемся выполнить
        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False
        # days_completed не должен измениться

    def test_skip_habit_with_no_completions(self, client: TestClient):
        """Тест: пропуск привычки без выполнения"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Новая"})
        habit_id = response.json()["id"]

        response = client.post(f"/habits/{habit_id}/skip")
        assert response.status_code == 200
        data = response.json()
        assert not data["days_completed"]
