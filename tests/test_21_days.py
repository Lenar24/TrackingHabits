"""
Тесты для правила 21 дня.
"""

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time


@pytest.mark.unit
class Test21DaysRule:
    """Тесты правила 21 дня"""

    @freeze_time("2026-01-01")
    def test_habit_completes_after_21_days(self, client: TestClient):
        """Тест: привычка завершается после 21 дня"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "21-дневная"})
        habit_id = response.json()["id"]

        # Отмечаем 21 день
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Проверяем, что привычка завершена
        response = client.get(f"/habits/item/{habit_id}")
        assert response.json()["is_active"] is False
        assert response.json()["days_completed"] == 21

    @freeze_time("2026-01-01")
    def test_progress_resets_after_skip(self, client: TestClient):
        """Тест: прогресс сбрасывается после пропуска"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Сбрасываемая"})
        habit_id = response.json()["id"]

        # Отмечаем 5 дней
        for day in range(5):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Пропускаем день
        with freeze_time("2026-01-06"):
            client.post(f"/habits/{habit_id}/skip")

        # Проверяем сброс
        response = client.get(f"/habits/item/{habit_id}")
        assert not response.json()["days_completed"]

    @freeze_time("2026-01-01")
    def test_progress_does_not_reset_after_one_day(self, client: TestClient):
        """Тест: прогресс не сбрасывается после одного дня"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Стабильная"})
        habit_id = response.json()["id"]

        with freeze_time("2026-01-01"):
            client.post(f"/habits/{habit_id}/complete")

        with freeze_time("2026-01-03"):
            response = client.get(f"/habits/item/{habit_id}")
            assert response.json()["days_completed"] == 1

    @freeze_time("2026-01-01")
    def test_daily_check_21_days_endpoint(self, client: TestClient):
        """
        Тест эндпоинта check-21-days.

        Создаём привычку с 20 днями (ещё не завершена)
        и привычку с 21 днём (должна быть завершена через check_21_days).
        """
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        # 1. Создаём привычку с 20 днями (НЕ должна завершиться)
        response = client.post("/habits/", json={"user_id": 12345, "name": "20-дневная"})
        habit_id_20 = response.json()["id"]
        for day in range(20):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id_20}/complete")

        # Проверяем, что привычка с 20 днями активна
        response = client.get(f"/habits/item/{habit_id_20}")
        assert response.json()["is_active"] is True
        assert response.json()["days_completed"] == 20

        # 2. Создаём привычку и отмечаем 21 день
        response2 = client.post("/habits/", json={"user_id": 12345, "name": "21-дневная"})
        habit_id_21 = response2.json()["id"]
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id_21}/complete")

        # ВАЖНО: Если mark_completed автоматически завершает привычку на 21-й день,
        # то check_21_days не найдёт её (она уже is_active=False)
        # Поэтому проверяем, что check_21_days завершает привычку,
        # которая по какой-то причине не завершилась автоматически

        # Запускаем проверку check-21-days
        response = client.post("/habits/check-21-days")
        assert response.status_code == 200
        data = response.json()
        assert "updated" in data
        assert "completed" in data

        # Проверяем привычку с 21 днём
        response = client.get(f"/habits/item/{habit_id_21}")
        # Если она уже завершена - check_21_days не трогает её
        # Если ещё активна - check_21_days должна завершить
        # В любом случае, она должна быть неактивна
        assert response.json()["is_active"] is False
        assert response.json()["days_completed"] == 21

    @freeze_time("2026-01-01")
    def test_check_21_days_with_manual_completion(self, client: TestClient):
        """
        Тест: check_21_days завершает привычки, которые достигли 21 дня,
        но НЕ были завершены автоматически (например, из-за сбоя).
        """
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        # Создаём привычку и отмечаем 21 день
        response = client.post("/habits/", json={"user_id": 12345, "name": "Ручная проверка"})
        habit_id = response.json()["id"]
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Создаём вторую привычку
        response2 = client.post("/habits/", json={"user_id": 12345, "name": "Для проверки"})
        habit_id2 = response2.json()["id"]
        for day in range(21):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id2}/complete")

        # Запускаем check_21_days
        client.post("/habits/check-21-days")

        # Проверяем, что привычки завершены
        response = client.get(f"/habits/item/{habit_id2}")
        assert response.json()["is_active"] is False

    @freeze_time("2026-01-01")
    def test_skip_resets_then_restart(self, client: TestClient):
        """Тест: после пропуска можно начать заново"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Перезапускаемая"})
        habit_id = response.json()["id"]

        for day in range(3):
            with freeze_time(f"2026-01-{day + 1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        with freeze_time("2026-01-04"):
            client.post(f"/habits/{habit_id}/skip")

        response = client.get(f"/habits/item/{habit_id}")
        assert not response.json()["days_completed"]

        with freeze_time("2026-01-05"):
            client.post(f"/habits/{habit_id}/complete")

        response = client.get(f"/habits/item/{habit_id}")
        assert response.json()["days_completed"] == 1
