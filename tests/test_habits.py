from datetime import date

import pytest
from fastapi.testclient import TestClient


def test_create_habit(client: TestClient):
    """Тест создания привычки"""
    # Создаём пользователя
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})

    response = client.post("/habits/", json={"user_id": 12345, "name": "Читать книги"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Читать книги"
    assert data["user_id"] == 12345
    assert data["is_active"] == True
    assert data["days_completed"] == 0
    assert data["max_days"] == 21


def test_get_habits(client: TestClient):
    """Тест получения списка привычек"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    client.post("/habits/", json={"user_id": 12345, "name": "Привычка 1"})
    client.post("/habits/", json={"user_id": 12345, "name": "Привычка 2"})

    response = client.get("/habits/12345")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Привычка 1"
    assert data[1]["name"] == "Привычка 2"


def test_get_habit_by_id(client: TestClient):
    """Тест получения привычки по ID"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Тестовая привычка"})
    habit_id = create_response.json()["id"]

    response = client.get(f"/habits/item/{habit_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Тестовая привычка"
    assert data["id"] == habit_id


def test_complete_habit(client: TestClient):
    """Тест отметки выполнения привычки"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Выполняемая привычка"})
    habit_id = create_response.json()["id"]

    response = client.post(f"/habits/{habit_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["days_completed"] == 1
    assert data["last_completed"] == str(date.today())


def test_skip_habit(client: TestClient):
    """Тест пропуска привычки"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Пропускаемая привычка"})
    habit_id = create_response.json()["id"]

    # Сначала выполняем
    client.post(f"/habits/{habit_id}/complete")

    # Затем пропускаем
    response = client.post(f"/habits/{habit_id}/skip")
    assert response.status_code == 200
    data = response.json()
    assert data["days_completed"] == 0
    assert data["last_completed"] is None


def test_complete_habit_early(client: TestClient):
    """Тест досрочного завершения привычки"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Досрочная привычка"})
    habit_id = create_response.json()["id"]

    response = client.post(f"/habits/{habit_id}/complete-early")
    assert response.status_code == 200
    data = response.json()
    assert data["is_active"] == False
    assert data["days_completed"] == 21
    assert data["completed_early"] == True


def test_delete_habit(client: TestClient):
    """Тест удаления привычки"""
    client.post("/users/", json={"user_id": 12345, "username": "habit_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Удаляемая привычка"})
    habit_id = create_response.json()["id"]

    response = client.delete(f"/habits/{habit_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Habit deleted"}

    # Проверяем, что привычка удалена
    get_response = client.get(f"/habits/item/{habit_id}")
    assert get_response.status_code == 404
