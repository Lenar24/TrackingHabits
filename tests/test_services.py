"""
Тесты сервисного слоя.
"""

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

from backend.app.models import Habit, User
from backend.app.schemas import HabitCreate, UserCreate
from backend.app.services.habit_service import HabitService
from backend.app.services.user_service import UserService


class TestHabitService:
    """Тесты сервиса привычек"""

    def test_create_habit(self, db_session):
        """Тест создания привычки через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit_data = HabitCreate(user_id=user.user_id, name="Test")
        habit = HabitService.create_habit(db_session, habit_data)

        assert habit.id is not None
        assert habit.name == "Test"
        assert habit.user_id == user.user_id

    def test_get_habits(self, db_session):
        """Тест получения привычек через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit = Habit(user_id=user.user_id, name="Test Habit", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        habits = HabitService.get_habits(db_session, user.user_id)
        assert len(habits) >= 1
        assert habits[0].name == "Test Habit"

    def test_mark_completed(self, db_session):
        """Тест отметки выполнения через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit = Habit(user_id=user.user_id, name="Test Habit", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        habit = HabitService.mark_completed(db_session, habit.id)
        assert habit.days_completed == 1
        assert habit.last_completed == date.today()

    def test_skip_habit(self, db_session):
        """Тест пропуска через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit = Habit(user_id=user.user_id, name="Test Habit", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        habit = HabitService.mark_completed(db_session, habit.id)
        assert habit.days_completed == 1

        habit = HabitService.mark_skipped(db_session, habit.id)
        assert not habit.days_completed

    def test_complete_early(self, db_session):
        """Тест досрочного завершения через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit = Habit(user_id=user.user_id, name="Test Habit", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        for _ in range(5):
            habit = HabitService.mark_completed(db_session, habit.id)

        habit = HabitService.complete_early(db_session, habit.id)
        assert habit.is_active is False
        assert habit.days_completed == 21
        assert habit.completed_early is True

    def test_get_habit_by_id(self, db_session):
        """Тест получения привычки по ID через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        habit = Habit(user_id=user.user_id, name="Test Habit", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        found_habit = HabitService.get_habit(db_session, habit.id)
        assert found_habit is not None
        assert found_habit.id == habit.id
        assert found_habit.name == "Test Habit"

    def test_get_habits_active_only(self, db_session):
        """Тест получения только активных привычек"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        active_habit = Habit(user_id=user.user_id, name="Active Habit", max_days=21)
        db_session.add(active_habit)
        db_session.commit()
        db_session.refresh(active_habit)

        completed_habit = Habit(
            user_id=user.user_id, name="Completed Habit", max_days=21, is_active=False, days_completed=21
        )
        db_session.add(completed_habit)
        db_session.commit()
        db_session.refresh(completed_habit)

        habits = HabitService.get_habits(db_session, user.user_id, active_only=True)
        assert len(habits) == 1
        assert habits[0].name == "Active Habit"

        all_habits = HabitService.get_habits(db_session, user.user_id, active_only=False)
        assert len(all_habits) == 2


class TestUserService:
    """Тесты сервиса пользователей"""

    def test_create_user(self, db_session):
        """Тест создания пользователя через сервис"""
        user_data = UserCreate(user_id=12345, username="test", chat_id=67890)
        user = UserService.create_user(db_session, user_data)

        assert user.id is not None
        assert user.user_id == 12345
        assert user.username == "test"
        assert user.chat_id == 67890

    def test_create_user_without_chat_id(self, db_session):
        """Тест создания пользователя без chat_id"""
        user_data = UserCreate(user_id=12345, username="test")
        user = UserService.create_user(db_session, user_data)

        assert user.id is not None
        assert user.user_id == 12345
        assert user.username == "test"
        assert user.chat_id is None

    def test_get_user(self, db_session):
        """Тест получения пользователя через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        found_user = UserService.get_user(db_session, user.user_id)
        assert found_user is not None
        assert found_user.user_id == user.user_id
        assert found_user.username == user.username

    def test_get_user_not_found(self, db_session):
        """Тест получения несуществующего пользователя"""
        user = UserService.get_user(db_session, 99999)
        assert user is None

    def test_update_chat_id(self, db_session):
        """Тест обновления chat_id через сервис"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        user = UserService.update_chat_id(db_session, user.user_id, 99999)
        assert user.chat_id == 99999

    def test_update_chat_id_user_not_found(self, db_session):
        """Тест обновления chat_id для несуществующего пользователя"""
        user = UserService.update_chat_id(db_session, 99999, 12345)
        assert user is None

    def test_create_duplicate_user(self, db_session):
        """
        Тест создания дублирующего пользователя.

        Так как user_id имеет уникальное ограничение,
        повторное создание с тем же user_id должно вызвать ошибку.
        """
        # Создаём пользователя
        user_data1 = UserCreate(user_id=12345, username="test1", chat_id=67890)
        user1 = UserService.create_user(db_session, user_data1)
        assert user1.id is not None
        assert user1.user_id == 12345

        # Пытаемся создать дубликат - должна быть ошибка
        user_data2 = UserCreate(user_id=12345, username="test2", chat_id=99999)

        # Ожидаем ошибку IntegrityError
        with pytest.raises(IntegrityError):
            UserService.create_user(db_session, user_data2)

        # Откатываем транзакцию после ошибки
        db_session.rollback()

    def test_create_user_with_same_chat_id(self, db_session):
        """Тест создания пользователей с одинаковым chat_id (это разрешено)"""
        user_data1 = UserCreate(user_id=12345, username="test1", chat_id=67890)
        user1 = UserService.create_user(db_session, user_data1)
        assert user1.id is not None

        user_data2 = UserCreate(user_id=67890, username="test2", chat_id=67890)
        user2 = UserService.create_user(db_session, user_data2)
        assert user2.id is not None
        assert user2.user_id == 67890
        assert user2.chat_id == 67890

    def test_create_user_with_very_long_username(self, db_session):
        """Тест создания пользователя с длинным username"""
        long_username = "a" * 255
        user_data = UserCreate(user_id=12345, username=long_username, chat_id=67890)
        user = UserService.create_user(db_session, user_data)

        assert user.id is not None
        assert user.user_id == 12345
        assert user.username == long_username
