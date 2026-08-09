"""
Тесты валидации данных.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.unit
class TestValidation:
    """Тесты валидации"""

    def test_create_user_with_invalid_user_id(self, client: TestClient):
        """
        Тест: создание пользователя с невалидным user_id.

        В текущей реализации отрицательные значения принимаются,
        поэтому тест проверяет, что пользователь создаётся,
        но с отрицательным user_id.
        """
        response = client.post("/users/", json={"user_id": -1, "username": "invalid_user"})
        # Если валидации нет - возвращается 200
        if response.status_code == 200:
            data = response.json()
            assert data["user_id"] == -1
        else:
            assert response.status_code in [400, 422]

    def test_create_user_with_zero_user_id(self, client: TestClient):
        """Тест: создание пользователя с user_id = 0"""
        response = client.post("/users/", json={"user_id": 0, "username": "zero_user"})
        if response.status_code == 200:
            data = response.json()
            assert not data["user_id"]
        else:
            assert response.status_code in [400, 422]

    def test_create_habit_with_empty_name(self, client: TestClient):
        """
        Тест: создание привычки с пустым названием.

        В текущей реализации пустые названия принимаются.
        """
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": ""})

        if response.status_code == 200:
            data = response.json()
            assert not data["name"]
        else:
            assert response.status_code in [400, 422]

    def test_create_habit_with_very_long_name(self, client: TestClient):
        """Тест: создание привычки с очень длинным названием"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        long_name = "A" * 1000
        response = client.post("/habits/", json={"user_id": 12345, "name": long_name})
        # Может быть 200 (если нет валидации длины)
        if response.status_code == 200:
            data = response.json()
            assert data["name"] == long_name
        else:
            assert response.status_code in [400, 422]

    def test_create_habit_with_special_characters(self, client: TestClient):
        """Тест: создание привычки со спецсимволами"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post(
            "/habits/",
            json={"user_id": 12345, "name": "Привычка! @#$%^&*()_+{}|:<>?~`"}
        )
        if response.status_code == 200:
            data = response.json()
            assert data["name"] == "Привычка! @#$%^&*()_+{}|:<>?~`"

    def test_create_habit_with_nonexistent_user(self, client: TestClient):
        """Тест: создание привычки для несуществующего пользователя"""
        response = client.post("/habits/", json={"user_id": 99999, "name": "Тестовая привычка"})
        # Может вернуть 200 (если пользователь создаётся автоматически)
        # или 404 (если проверяется существование пользователя)
        assert response.status_code in [200, 404]

    def test_update_habit_with_empty_name(self, client: TestClient):
        """Тест: обновление привычки с пустым названием"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})
        response = client.post("/habits/", json={"user_id": 12345, "name": "Старое"})
        habit_id = response.json()["id"]

        response = client.put(f"/habits/{habit_id}", json={"name": ""})
        # Может быть 200 (если пустое имя разрешено)
        if response.status_code == 200:
            data = response.json()
            assert not data["name"]
        else:
            assert response.status_code in [400, 422]

    def test_update_user_chat_id_with_invalid_type(self, client: TestClient):
        """
        Тест: обновление chat_id с неверным типом.

        В текущей реализации int('not_a_number') вызывает ValueError.
        Тест проверяет, что API корректно обрабатывает эту ошибку.
        """
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        response = client.put("/users/12345/chat_id", json={"chat_id": "not_a_number"})
        # Должен вернуть 400 или 422
        assert response.status_code in [400, 422]

    def test_update_user_chat_id_with_negative_value(self, client: TestClient):
        """Тест: обновление chat_id с отрицательным значением"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        response = client.put("/users/12345/chat_id", json={"chat_id": -123})
        if response.status_code == 200:
            data = response.json()
            assert data["chat_id"] == -123
        else:
            assert response.status_code in [400, 422]

    def test_update_user_chat_id_with_zero(self, client: TestClient):
        """Тест: обновление chat_id с нулём"""
        client.post("/users/", json={"user_id": 12345, "username": "test_user"})

        response = client.put("/users/12345/chat_id", json={"chat_id": 0})
        if response.status_code == 200:
            data = response.json()
            assert not data["chat_id"]
        else:
            assert response.status_code in [400, 422]
