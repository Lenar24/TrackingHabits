import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.models import Habit, HabitLog, User
from backend.app.utils.database import Base, get_db

# Используем PostgreSQL для тестов
TEST_DATABASE_URL = "postgresql://postgresql:postgresql@localhost:5432/test_habit_tracker"

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    # Создаём таблицы заново для каждого теста
    Base.metadata.drop_all(bind=engine)  # Удаляем всё
    Base.metadata.create_all(bind=engine)  # Создаём заново

    with TestClient(app) as test_client:
        yield test_client

    # После теста закрываем соединения
    engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_user(db_session):
    # Проверяем, есть ли уже пользователь
    user = db_session.query(User).filter(User.user_id == 12345).first()
    if not user:
        user = User(user_id=12345, chat_id=12345, username="test_user")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_habit(db_session, test_user):
    from datetime import date

    habit = Habit(user_id=test_user.user_id, name="Тестовая привычка", max_days=21, last_updated=date.today())
    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)
    return habit
