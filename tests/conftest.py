"""
Общие фикстуры для всех тестов.
"""

import pytest
from datetime import date, datetime, timezone
from typing import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.main import app
from backend.app.models import Base, User, Habit, HabitLog
from backend.app.utils.database import get_db
from backend.app.utils.auth import create_access_token
from backend.app.core.config import settings


# ============ DATABASE FIXTURES ============

@pytest.fixture(scope="function")
def db_engine():
    """Создаёт тестовый движок SQLite в памяти."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Включаем foreign keys в SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Создаёт тестовую сессию БД."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session) -> TestClient:
    """Создаёт тестовый клиент FastAPI."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# ============ USER FIXTURES ============

@pytest.fixture
def test_user(db_session) -> User:
    """Создаёт тестового пользователя."""
    user = User(
        max_user_id=12345,
        chat_id=67890,
        username="test_user",
        is_admin=False,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_admin(db_session) -> User:
    """Создаёт тестового администратора."""
    admin = User(
        max_user_id=99999,
        chat_id=88888,
        username="admin_user",
        is_admin=True,
        is_active=True,
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture
def test_user2(db_session) -> User:
    """Создаёт второго пользователя."""
    user = User(
        max_user_id=54321,
        chat_id=98765,
        username="test_user2",
        is_admin=False,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ============ HABIT FIXTURES ============

@pytest.fixture
def test_habit(db_session, test_user) -> Habit:
    """Создаёт тестовую привычку."""
    habit = Habit(
        user_id=test_user.id,
        name="Утренняя зарядка",
        description="15 минут",
        max_days=21,
        days_completed=0,
        is_active=True,
    )
    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)
    return habit


@pytest.fixture
def test_habit_completed_today(db_session, test_user) -> Habit:
    """Создаёт привычку, выполненную сегодня."""
    habit = Habit(
        user_id=test_user.id,
        name="Выполненная привычка",
        description="Тест",
        max_days=21,
        days_completed=1,
        last_completed=date.today(),
        is_active=True,
    )
    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)
    return habit


@pytest.fixture
def test_habit_7_days(db_session, test_user) -> Habit:
    """Создаёт привычку с 7 днями выполнения (для досрочного завершения)."""
    habit = Habit(
        user_id=test_user.id,
        name="Привычка 7 дней",
        description="Тест",
        max_days=21,
        days_completed=7,
        last_completed=date.today(),
        is_active=True,
    )
    db_session.add(habit)
    db_session.commit()
    db_session.refresh(habit)
    return habit


@pytest.fixture
def test_habit_log(db_session, test_habit) -> HabitLog:
    """Создаёт тестовый лог выполнения."""
    log = HabitLog(
        habit_id=test_habit.id,
        date=date.today(),
        completed=True,
    )
    db_session.add(log)
    db_session.commit()
    db_session.refresh(log)
    return log


# ============ AUTH FIXTURES ============

@pytest.fixture
def test_token(test_user) -> str:
    """Создаёт JWT токен для тестового пользователя."""
    return create_access_token({
        "sub": str(test_user.id),
        "user_id": test_user.id,
        "max_user_id": test_user.max_user_id,
        "chat_id": test_user.chat_id,
    })


@pytest.fixture
def admin_token(test_admin) -> str:
    """Создаёт JWT токен для администратора."""
    return create_access_token({
        "sub": str(test_admin.id),
        "user_id": test_admin.id,
        "max_user_id": test_admin.max_user_id,
        "chat_id": test_admin.chat_id,
    })


@pytest.fixture
def auth_headers(test_token) -> dict:
    """Заголовки с JWT токеном."""
    return {"Authorization": f"Bearer {test_token}"}


@pytest.fixture
def admin_headers(admin_token) -> dict:
    """Заголовки с JWT токеном администратора."""
    return {"Authorization": f"Bearer {admin_token}"}


# ============ TIME FIXTURES ============

@pytest.fixture
def fixed_date():
    """Фиксированная дата для тестов."""
    return date(2026, 9, 12)


@pytest.fixture
def fixed_datetime():
    """Фиксированное время для тестов."""
    return datetime(2026, 9, 12, 12, 0, 0, tzinfo=timezone.utc)
