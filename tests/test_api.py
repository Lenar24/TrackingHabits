import pytest
from fastapi.testclient import TestClient


def test_read_root(client: TestClient):
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Habit Tracker API is running"}


def test_health_check(client: TestClient):
    """Тест проверки здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_user(client: TestClient):
    """Тест создания пользователя"""
    response = client.post("/users/", json={"user_id": 99999, "username": "new_user", "chat_id": 99999})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 99999
    assert data["username"] == "new_user"
    assert data["chat_id"] == 99999


def test_get_user(client: TestClient):
    """Тест получения пользователя"""
    # Сначала создаём пользователя
    client.post("/users/", json={"user_id": 88888, "username": "get_user"})

    response = client.get("/users/88888")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 88888
    assert data["username"] == "get_user"


def test_get_nonexistent_user(client: TestClient):
    """Тест получения несуществующего пользователя"""
    response = client.get("/users/9999999")
    assert response.status_code == 404


def test_get_all_users(client: TestClient):
    """Тест получения всех пользователей"""
    client.post("/users/", json={"user_id": 11111, "username": "user1"})
    client.post("/users/", json={"user_id": 22222, "username": "user2"})

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
