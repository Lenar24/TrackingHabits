"""
Тесты для эндпоинтов статистики привычек.
"""

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time


@pytest.mark.unit
class TestStatsAPI:
    """Тесты API статистики"""

    def test_get_stats_empty(self, client: TestClient):
        """Тест статистики без привычек"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_stats_nonexistent_user(self, client: TestClient):
        """Тест статистики для несуществующего пользователя"""
        response = client.get("/habits/99999/stats")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_stats_with_one_habit(self, client: TestClient):
        """Тест статистики с одной привычкой"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post(
            "/habits/",
            json={"user_id": 12345, "name": "Статистическая привычка", "description": "Описание для статистики"},
        )
        habit_id = create_response.json()["id"]

        # Выполняем 5 раз (используем freeze_time для разных дней)
        with freeze_time("2026-01-01"):
            for day in range(5):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Статистическая привычка"
        assert data[0]["days_completed"] >= 1
        assert data[0]["is_active"] is True

    def test_get_stats_with_multiple_habits(self, client: TestClient):
        """Тест статистики с несколькими привычками"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        # Создаём две привычки
        resp1 = client.post("/habits/", json={"user_id": 12345, "name": "Привычка 1"})
        habit_id1 = resp1.json()["id"]

        resp2 = client.post("/habits/", json={"user_id": 12345, "name": "Привычка 2"})
        habit_id2 = resp2.json()["id"]

        # Выполняем первую 3 раза
        with freeze_time("2026-01-01"):
            for day in range(3):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id1}/complete")

        # Выполняем вторую 7 раз
        with freeze_time("2026-01-10"):
            for day in range(7):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id2}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2

        for habit in data:
            if habit["name"] == "Привычка 1":
                assert habit["days_completed"] >= 1
            elif habit["name"] == "Привычка 2":
                assert habit["days_completed"] >= 1

    def test_stats_after_habit_completion(self, client: TestClient):
        """Тест статистики после выполнения привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Привычка для статистики"})
        habit_id = create_response.json()["id"]

        # Проверяем начальную статистику
        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert not data[0]["days_completed"]

        # Выполняем привычку
        with freeze_time("2026-01-01"):
            client.post(f"/habits/{habit_id}/complete")

        # Проверяем обновлённую статистику
        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert data[0]["days_completed"] >= 1

    def test_stats_after_skip(self, client: TestClient):
        """Тест статистики после пропуска"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Привычка для пропуска"})
        habit_id = create_response.json()["id"]

        # Выполняем 3 раза
        with freeze_time("2026-01-01"):
            for day in range(3):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        # Проверяем статистику
        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["days_completed"] >= 1

        # Пропускаем
        with freeze_time("2026-01-04"):
            client.post(f"/habits/{habit_id}/skip")

        # Проверяем обновлённую статистику
        response = client.get("/habits/12345/stats")
        data = response.json()
        assert not data[0]["days_completed"]

    @freeze_time("2026-01-01")
    def test_stats_best_streak(self, client: TestClient):
        """Тест лучшей серии в статистике"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Серийная привычка"})
        habit_id = create_response.json()["id"]

        # Выполняем 3 дня подряд
        for day in range(3):
            with freeze_time(f"2026-01-{day+1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Пропускаем день
        with freeze_time("2026-01-04"):
            client.post(f"/habits/{habit_id}/skip")

        # Выполняем ещё 2 дня
        for day in range(5, 7):
            with freeze_time(f"2026-01-{day:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["best_streak"] >= 1

    @freeze_time("2026-01-01")
    def test_stats_last_7_days(self, client: TestClient):
        """Тест статистики за последние 7 дней"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Еженедельная привычка"})
        habit_id = create_response.json()["id"]

        # Отмечаем 5 дней из 7
        for day in range(1, 8):
            with freeze_time(f"2026-01-{day:02d}"):
                if not day % 2:
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert "last_7_days" in data[0]
        assert len(data[0]["last_7_days"]) >= 1

    def test_stats_completed_habit(self, client: TestClient):
        """Тест статистики для завершённой привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Завершаемая привычка"})
        habit_id = create_response.json()["id"]

        # Выполняем 21 раз
        with freeze_time("2026-01-01"):
            for day in range(21):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Завершаемая привычка"
        assert data[0]["days_completed"] == 21
        assert data[0]["is_active"] is False

    def test_stats_completed_early(self, client: TestClient):
        """Тест статистики для досрочно завершённой привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Досрочная привычка"})
        habit_id = create_response.json()["id"]

        # Выполняем 5 раз
        with freeze_time("2026-01-01"):
            for day in range(5):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        # Завершаем досрочно
        client.post(f"/habits/{habit_id}/complete-early")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Досрочная привычка"
        assert data[0]["days_completed"] == 21
        assert data[0]["is_active"] is False

    def test_stats_response_structure(self, client: TestClient):
        """Тест структуры ответа статистики"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Структурная привычка"})
        habit_id = create_response.json()["id"]

        # Выполняем несколько раз
        with freeze_time("2026-01-01"):
            for day in range(3):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        expected_fields = [
            "id",
            "name",
            "is_active",
            "days_completed",
            "max_days",
            "total_logs",
            "completed_logs",
            "best_streak",
            "last_7_days",
        ]
        for field in expected_fields:
            assert field in data[0], f"Поле {field} отсутствует"

    def test_stats_best_streak_initial(self, client: TestClient):
        """Тест лучшей серии без выполнения"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        # Создаём привычку, но ID не нужен
        client.post("/habits/", json={"user_id": 12345, "name": "Новая привычка"})

        response = client.get("/habits/12345/stats")
        data = response.json()
        assert not data[0]["best_streak"]

    def test_stats_completed_logs_vs_total_logs(self, client: TestClient):
        """Тест соотношения выполненных и общих логов"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Смешанная привычка"})
        habit_id = create_response.json()["id"]

        with freeze_time("2026-01-01"):
            # Выполняем 5 раз
            for day in range(5):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

            # Пропускаем 3 раза
            for day in range(5, 8):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/skip")

            # Снова выполняем 2 раза
            for day in range(8, 10):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["total_logs"] >= 5
        assert data[0]["completed_logs"] >= 5

    @freeze_time("2026-01-01")
    def test_stats_with_habit_progress(self, client: TestClient):
        """Тест статистики с прогрессом привычки"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Прогрессивная привычка"})
        habit_id = create_response.json()["id"]

        # Проверяем начальный прогресс
        response = client.get("/habits/12345/stats")
        data = response.json()
        assert not data[0]["days_completed"]

        # Выполняем 10 раз
        for day in range(10):
            with freeze_time(f"2026-01-{day+1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Проверяем прогресс
        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["days_completed"] == 10
        assert data[0]["max_days"] == 21

        # Выполняем ещё 11 раз (всего 21)
        for day in range(10, 21):
            with freeze_time(f"2026-01-{day+1:02d}"):
                client.post(f"/habits/{habit_id}/complete")

        # Проверяем завершение
        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["days_completed"] == 21
        assert data[0]["is_active"] is False


@pytest.mark.slow
class TestStatsSlow:  # pylint: disable=too-few-public-methods
    """Медленные тесты статистики"""

    @freeze_time("2026-01-01")
    def test_stats_after_many_days(self, client: TestClient):
        """Тест статистики после многих дней выполнения"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Долгая привычка"})
        habit_id = create_response.json()["id"]

        # Выполняем 30 дней с пропусками
        for day in range(1, 31):
            with freeze_time(f"2026-01-{day:02d}"):
                if not day % 2:
                    client.post(f"/habits/{habit_id}/complete")
                else:
                    client.post(f"/habits/{habit_id}/skip")

        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["total_logs"] == 30
        assert data[0]["completed_logs"] == 15


@pytest.mark.integration
class TestStatsIntegration:
    """Интеграционные тесты статистики"""

    def test_stats_user_habit_relationship(self, client: TestClient):
        """Интеграционный тест: статистика связывает пользователя и привычку"""
        user_response = client.post("/users/", json={"user_id": 88888, "username": "integration_stats_user"})
        assert user_response.status_code == 200
        user_data = user_response.json()

        habit_response = client.post("/habits/", json={"user_id": 88888, "name": "Интеграционная привычка"})
        assert habit_response.status_code == 200

        with freeze_time("2026-01-01"):
            client.post(f"/habits/{habit_response.json()['id']}/complete")

        response = client.get(f"/habits/{user_data['user_id']}/stats")
        assert response.status_code == 200
        stats = response.json()
        assert len(stats) == 1
        assert stats[0]["id"] == habit_response.json()["id"]
        assert stats[0]["name"] == "Интеграционная привычка"
        assert stats[0]["days_completed"] == 1

    def test_stats_after_complete_and_skip_cycle(self, client: TestClient):
        """Интеграционный тест: статистика после циклов выполнение/пропуск"""
        client.post("/users/", json={"user_id": 12345, "username": "stats_user"})

        create_response = client.post("/habits/", json={"user_id": 12345, "name": "Циклическая привычка"})
        habit_id = create_response.json()["id"]

        with freeze_time("2026-01-01"):
            # Цикл: выполнить 3 раза, пропустить 2 раза, выполнить 4 раза
            for day in range(3):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

            for day in range(3, 5):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/skip")

            for day in range(5, 9):
                with freeze_time(f"2026-01-{day+1:02d}"):
                    client.post(f"/habits/{habit_id}/complete")

        response = client.get("/habits/12345/stats")
        data = response.json()
        assert data[0]["total_logs"] >= 5
        assert data[0]["completed_logs"] >= 5
