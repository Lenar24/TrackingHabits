from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text


@pytest.mark.skip(reason="Требуется доработка тестовой среды (проблема с имитацией дней)")
def test_21_days_rule(client: TestClient):
    """Тест правила 21 дня"""
    client.post("/users/", json={"user_id": 12345, "username": "test_user"})
    create_response = client.post("/habits/", json={"user_id": 12345, "name": "21-дневная привычка"})
    habit_id = create_response.json()["id"]

    from backend.app.utils.database import SessionLocal

    current_date = date.today()

    for day in range(1, 22):
        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["days_completed"] == day, f"День {day}: ожидалось {day}, получено {data['days_completed']}"

        if day < 21:
            current_date = current_date + timedelta(days=1)
            db = SessionLocal()
            try:
                db.execute(
                    text("UPDATE habits SET last_updated = :date, last_completed = NULL WHERE id = :id"),
                    {"date": current_date, "id": habit_id},
                )
                db.commit()
            finally:
                db.close()

    final_response = client.get(f"/habits/item/{habit_id}")
    final_data = final_response.json()
    assert final_data["days_completed"] == 21
    assert final_data["is_active"] == False


def test_21_days_skip_reset(client: TestClient):
    """Тест сброса при пропуске"""
    client.post("/users/", json={"user_id": 12345, "username": "test_user"})

    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Привычка с пропуском"})
    habit_id = create_response.json()["id"]

    for _ in range(5):
        client.post(f"/habits/{habit_id}/complete")

    client.post(f"/habits/{habit_id}/skip")

    response = client.get(f"/habits/item/{habit_id}")
    data = response.json()
    assert data["days_completed"] == 0
    assert data["last_completed"] is None


@pytest.mark.skip(reason="Требуется доработка тестовой среды (проблема с имитацией дней)")
def test_21_days_check_endpoint(client: TestClient):
    """Тест эндпоинта проверки правила 21 дня"""
    client.post("/users/", json={"user_id": 12345, "username": "test_user"})

    create_response = client.post("/habits/", json={"user_id": 12345, "name": "Проверяемая привычка"})
    habit_id = create_response.json()["id"]

    from backend.app.utils.database import SessionLocal

    current_date = date.today()

    for day in range(1, 22):
        response = client.post(f"/habits/{habit_id}/complete")
        assert response.status_code == 200

        if day < 21:
            current_date = current_date + timedelta(days=1)
            db = SessionLocal()
            try:
                db.execute(
                    text("UPDATE habits SET last_updated = :date, last_completed = NULL WHERE id = :id"),
                    {"date": current_date, "id": habit_id},
                )
                db.commit()
            finally:
                db.close()

    response = client.post("/habits/check-21-days")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] >= 1

    final_response = client.get(f"/habits/item/{habit_id}")
    final_data = final_response.json()
    assert final_data["days_completed"] == 21
    assert final_data["is_active"] == False
