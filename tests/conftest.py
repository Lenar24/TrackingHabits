"""
Конфигурация для тестов с использованием SQLite в памяти.
Все тесты изолированы и не влияют друг на друга.
"""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.models import Habit, User
from backend.app.utils.database import Base, get_db

# НАСТРОЙКА ТЕСТОВОЙ БАЗЫ ДАННЫХ

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    echo=False,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ФУНКЦИИ УПРАВЛЕНИЯ ТАБЛИЦАМИ


def create_tables():
    """Создает все таблицы в тестовой БД"""
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """Удаляет все таблицы из тестовой БД"""
    Base.metadata.drop_all(bind=engine)


# ПЕРЕОПРЕДЕЛЕНИЕ ЗАВИСИМОСТЕЙ FASTAPI


def override_get_db():
    """Переопределяет зависимость get_db для использования тестовой БД"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ФИКСТУРЫ


@pytest.fixture(scope="function")
def db_session():
    """
    Фикстура для тестовой сессии базы данных.
    Создаёт таблицы перед тестом и удаляет после.
    """
    create_tables()

    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.rollback()
        db.close()
        drop_tables()


@pytest.fixture(scope="function")
def client():
    """
    Фикстура для тестового клиента FastAPI.
    ИСПОЛЬЗУЕТ ТУ ЖЕ БД, ЧТО И СЕССИЯ
    """
    create_tables()

    def _override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as test_client:
        yield test_client

    drop_tables()


@pytest.fixture(scope="function")
def client_with_db():
    """
    Альтернативная фикстура: клиент + сессия БД.
    """
    create_tables()

    db = TestingSessionLocal()

    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as test_client:
        yield test_client, db

    db.close()
    drop_tables()


@pytest.fixture(scope="function")
def test_user_data():
    """Фикстура с тестовыми данными пользователя"""
    return {"user_id": 123456789, "username": "test_user", "chat_id": 987654321}


@pytest.fixture(scope="function")
def test_user(client):
    """
    Фикстура для тестового пользователя в БД.
    Использует client для создания пользователя через API.
    """
    response = client.post("/users/", json={"user_id": 123456789, "username": "test_user", "chat_id": 987654321})
    assert response.status_code == 200, f"Ошибка создания пользователя: {response.text}"
    return response.json()


@pytest.fixture(scope="function")
def test_habit(client, test_user):
    """Фикстура для тестовой привычки в БД"""
    response = client.post(
        "/habits/",
        json={
            "user_id": test_user["user_id"],
            "name": "Тестовая привычка",
            "description": "Описание тестовой привычки",
        },
    )
    assert response.status_code == 200, f"Ошибка создания привычки: {response.text}"
    return response.json()


@pytest.fixture(scope="function")
def test_habit_with_progress(client, test_user):
    """Фикстура для привычки с прогрессом"""
    # Создаём привычку
    response = client.post("/habits/", json={"user_id": test_user["user_id"], "name": "Привычка с прогрессом"})
    assert response.status_code == 200
    habit = response.json()

    # Отмечаем несколько дней
    for _ in range(5):
        client.post(f"/habits/{habit['id']}/complete")

    return client.get(f"/habits/item/{habit['id']}").json()


@pytest.fixture(scope="function")
def test_habit_completed(client, test_user):
    """Фикстура для завершённой привычки"""
    # Создаём привычку
    response = client.post("/habits/", json={"user_id": test_user["user_id"], "name": "Завершённая привычка"})
    assert response.status_code == 200
    habit = response.json()

    # Отмечаем 21 день
    for _ in range(21):
        client.post(f"/habits/{habit['id']}/complete")

    return client.get(f"/habits/item/{habit['id']}").json()


@pytest.fixture(scope="function")
def test_habit_log(client, test_habit):
    """Фикстура для тестового лога привычки"""
    response = client.post(f"/habits/{test_habit['id']}/complete")
    assert response.status_code == 200
    return response.json()


@pytest.fixture(scope="function")
def multiple_test_habits(client, test_user):
    """Фикстура для нескольких привычек"""
    habits = []
    names = ["Привычка 1", "Привычка 2", "Привычка 3"]

    for name in names:
        response = client.post("/habits/", json={"user_id": test_user["user_id"], "name": name})
        assert response.status_code == 200
        habits.append(response.json())

    return habits


# МАРКЕРЫ ДЛЯ ТЕСТОВ


def pytest_configure(config):
    """Настройка маркеров для pytest"""
    config.addinivalue_line("markers", "unit: marks tests as unit tests")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "db: marks tests that require database")


# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ


def create_test_user_via_db(session, user_id=12345, chat_id=12345, username="test_user"):
    """Вспомогательная функция для создания пользователя напрямую в БД"""
    user = User(user_id=user_id, chat_id=chat_id, username=username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_test_habit_via_db(session, user_id, name="Тестовая привычка", days=0):
    """Вспомогательная функция для создания привычки напрямую в БД"""
    habit = Habit(user_id=user_id, name=name, max_days=21, days_completed=days, last_updated=date.today())
    session.add(habit)
    session.commit()
    session.refresh(habit)
    return habit
