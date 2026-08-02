import pytest
from fastapi.testclient import TestClient

from backend.app.models import User


def test_update_chat_id(client: TestClient):
    """Тест обновления chat_id"""
    # Создаём пользователя
    client.post("/users/", json={"user_id": 77777, "username": "chat_user"})

    # Обновляем chat_id
    response = client.put("/users/77777/chat_id", json={"chat_id": 88888})
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == 88888


def test_duplicate_user(client: TestClient):
    """Тест создания дублирующего пользователя"""
    client.post("/users/", json={"user_id": 55555, "username": "dup_user"})

    # Попытка создать дубликат
    response = client.post("/users/", json={"user_id": 55555, "username": "dup_user_2"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 55555
    assert data["username"] == "dup_user"  # Имя не должно измениться
