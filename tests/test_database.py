"""
Тесты базы данных.
"""

from datetime import date

from sqlalchemy import text

from backend.app.models import Habit, HabitLog, User


class TestDatabase:
    """Тесты БД"""

    def test_database_connection(self, db_session):
        """Тест подключения к БД"""
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1

    def test_create_user_in_db(self, db_session):
        """Тест создания пользователя в БД"""
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        result = db_session.query(User).filter(User.user_id == 12345).first()
        assert result is not None
        assert result.username == "test_user"
        assert result.chat_id == 67890

    def test_create_habit_in_db(self, db_session):
        """Тест создания привычки в БД"""
        # Сначала создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(
            user_id=user.user_id,
            name="Тестовая привычка",
            description="Описание",
            max_days=21,
            last_updated=date.today(),
        )
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Проверяем
        result = db_session.query(Habit).filter(Habit.name == "Тестовая привычка").first()
        assert result is not None
        assert result.user_id == user.user_id
        assert result.name == "Тестовая привычка"
        assert result.description == "Описание"
        assert result.max_days == 21
        assert result.is_active is True
        assert not result.days_completed

    def test_create_log_in_db(self, db_session):
        """Тест создания лога в БД"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(
            user_id=user.user_id,
            name="Привычка для логов",
            max_days=21,
            last_updated=date.today()
        )
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Создаём лог
        log = HabitLog(habit_id=habit.id, date=date.today(), completed=True)
        db_session.add(log)
        db_session.commit()
        db_session.refresh(log)

        # Проверяем
        result = db_session.query(HabitLog).filter(HabitLog.habit_id == habit.id).first()
        assert result is not None
        assert result.habit_id == habit.id
        assert result.date == date.today()
        assert result.completed is True

    def test_create_multiple_logs(self, db_session):
        """Тест создания нескольких логов для одной привычки"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(
            user_id=user.user_id,
            name="Привычка с логами",
            max_days=21,
            last_updated=date.today()
        )
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Создаём несколько логов
        for i in range(5):
            log = HabitLog(
                habit_id=habit.id,
                date=date.today() - __import__("datetime").timedelta(days=i),
                completed=(i % 2 == 0),  # Чётные - выполнены, нечётные - нет
            )
            db_session.add(log)

        db_session.commit()

        # Проверяем количество
        logs = db_session.query(HabitLog).filter(HabitLog.habit_id == habit.id).all()
        assert len(logs) == 5

        # Проверяем статусы
        completed = (
            db_session.query(HabitLog)
            .filter(HabitLog.habit_id == habit.id, HabitLog.completed == True)
            .count()
        )
        assert completed == 3  # 0, 2, 4 - чётные

    def test_user_habit_relationship(self, db_session):
        """Тест связи пользователь-привычка"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(user_id=user.user_id, name="Связанная привычка", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Проверяем связь через пользователя
        user_with_habits = db_session.query(User).filter(User.user_id == 12345).first()
        assert len(user_with_habits.habits) == 1
        assert user_with_habits.habits[0].name == "Связанная привычка"

        # Проверяем связь через привычку
        habit_with_user = db_session.query(Habit).filter(Habit.id == habit.id).first()
        assert habit_with_user.user.user_id == 12345

    def test_habit_log_relationship(self, db_session):
        """Тест связи привычка-лог"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(user_id=user.user_id, name="Привычка с логами", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Создаём лог
        log = HabitLog(habit_id=habit.id, date=date.today(), completed=True)
        db_session.add(log)
        db_session.commit()
        db_session.refresh(log)

        # Проверяем связь через привычку
        habit_with_logs = db_session.query(Habit).filter(Habit.id == habit.id).first()
        assert len(habit_with_logs.logs) == 1
        assert habit_with_logs.logs[0].completed is True

        # Проверяем связь через лог
        log_with_habit = db_session.query(HabitLog).filter(HabitLog.id == log.id).first()
        assert log_with_habit.habit.id == habit.id

    def test_cascade_delete(self, db_session):
        """Тест каскадного удаления: удаление привычки удаляет логи"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём привычку
        habit = Habit(user_id=user.user_id, name="Привычка для каскадного удаления", max_days=21)
        db_session.add(habit)
        db_session.commit()
        db_session.refresh(habit)

        # Создаём логи
        for i in range(3):
            log = HabitLog(
                habit_id=habit.id,
                date=date.today() - __import__("datetime").timedelta(days=i),
                completed=True
            )
            db_session.add(log)

        db_session.commit()

        # Проверяем количество логов
        logs_before = db_session.query(HabitLog).filter(HabitLog.habit_id == habit.id).count()
        assert logs_before == 3

        # Удаляем привычку
        db_session.delete(habit)
        db_session.commit()

        # Проверяем, что логи удалены
        logs_after = db_session.query(HabitLog).filter(HabitLog.habit_id == habit.id).count()
        assert not logs_after

    def test_user_habits_count(self, db_session):
        """Тест подсчёта привычек у пользователя"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём несколько привычек
        for i in range(3):
            habit = Habit(user_id=user.user_id, name=f"Привычка {i + 1}", max_days=21)
            db_session.add(habit)

        db_session.commit()

        # Проверяем количество
        count = db_session.query(Habit).filter(Habit.user_id == user.user_id).count()
        assert count == 3

    def test_active_habits_count(self, db_session):
        """Тест подсчёта активных привычек"""
        # Создаём пользователя
        user = User(user_id=12345, username="test_user", chat_id=67890)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Создаём активную привычку
        active = Habit(user_id=user.user_id, name="Активная", max_days=21, is_active=True)
        db_session.add(active)

        # Создаём завершённую привычку
        completed = Habit(
            user_id=user.user_id,
            name="Завершённая",
            max_days=21,
            is_active=False,
            days_completed=21
        )
        db_session.add(completed)

        db_session.commit()

        # Проверяем количество активных
        active_count = (
            db_session.query(Habit)
            .filter(Habit.user_id == user.user_id, Habit.is_active == True)
            .count()
        )
        assert active_count == 1

        # Проверяем количество завершённых
        completed_count = (
            db_session.query(Habit)
            .filter(Habit.user_id == user.user_id, Habit.is_active == False)
            .count()
        )
        assert completed_count == 1
