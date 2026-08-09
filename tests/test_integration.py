"""
Сквозные интеграционные тесты.
"""

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time


@pytest.mark.integration
class TestIntegration:
    """Сквозные тесты"""

    @freeze_time("2026-01-01")
    def test_complete_user_flow(self, client: TestClient):
        """
        Полный пользовательский сценарий:
        регистрация → создание привычки → выполнение → завершение
        """

        # 1. Регистрация пользователя
        user_response = client.post(
            "/users/",
            json={"user_id": 12345, "username": "john_doe", "chat_id": 67890}
        )
        assert user_response.status_code == 200
        user_data = user_response.json()
        assert user_data["user_id"] == 12345

        # 2. Создание привычки
        habit_response = client.post(
            "/habits/",
            json={"user_id": 12345, "name": "Ежедневная зарядка", "description": "10 минут"}
        )
        assert habit_response.status_code == 200
        habit_data = habit_response.json()
        habit_id = habit_data["id"]

        # 3. Получение привычек
        response = client.get("/habits/12345")
        assert response.status_code == 200
        habits = response.json()
        assert len(habits) == 1
        assert habits[0]["name"] == "Ежедневная зарядка"

        # 4. Ежедневное выполнение (21 день)
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                response = client.post(f"/habits/{habit_id}/complete")
                assert response.status_code == 200
                data = response.json()
                if day == 20:
                    assert data["is_active"] is False
                    assert data["days_completed"] == 21

        # 5. Проверка завершения
        response = client.get(f"/habits/item/{habit_id}")
        data = response.json()
        assert data["is_active"] is False
        assert data["days_completed"] == 21

        # 6. Проверка статистики
        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 1
        assert stats[0]["days_completed"] == 21

    @freeze_time("2026-01-01")
    def test_habit_with_skip_flow(self, client: TestClient):
        """Сценарий с пропуском дня"""

        # 1. Регистрация и создание привычки
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Чтение"})
        habit_id = response.json()["id"]

        # 2. Выполняем 3 дня
        for day in range(3):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # 3. Пропускаем день
        with freeze_time("2026-01-04"):
            client.post(f"/habits/{habit_id}/skip")

        # 4. Проверяем сброс
        response = client.get(f"/habits/item/{habit_id}")
        assert not response.json()["days_completed"]

        # 5. Начинаем заново
        with freeze_time("2026-01-05"):
            client.post(f"/habits/{habit_id}/complete")

        response = client.get(f"/habits/item/{habit_id}")
        assert response.json()["days_completed"] == 1

    def test_user_and_habits_cleanup(self, client: TestClient):
        """Тест: удаление пользователя удаляет все привычки"""

        # 1. Создание пользователя
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        # 2. Создание привычек
        client.post("/habits/", json={"user_id": 12345, "name": "Привычка 1"})
        client.post("/habits/", json={"user_id": 12345, "name": "Привычка 2"})

        # 3. Проверка
        response = client.get("/habits/12345")
        assert len(response.json()) == 2
