"""
Класс HabitService реализует бизнес-логику работы с привычками.
Содержит методы для создания, получения, обновления привычек,
а также для отметки выполнения, пропуска и завершения.
Реализует систему отслеживания привычек по методу "21 день".
"""

from datetime import date, datetime, timedelta

from sqlalchemy.orm import Session

from ..models import Habit, HabitLog
from ..schemas import HabitCreate


class HabitService:
    """Класс HabitService"""

    @staticmethod
    def create_habit(db: Session, habit: HabitCreate):
        """Создание новой привычки в базе данных."""
        db_habit = Habit(
            user_id=habit.user_id,
            name=habit.name,
            description=habit.description,
            last_updated=date.today(),
        )
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit

    @staticmethod
    def get_habits(db: Session, user_id: int, active_only: bool = True):
        """Получение списка привычек пользователя с возможностью фильтрации."""
        query = db.query(Habit).filter(Habit.user_id == user_id)
        if active_only:
            query = query.filter(Habit.is_active == True)  # pylint: disable=singleton-comparison
        return query.all()

    @staticmethod
    def get_habit(db: Session, habit_id: int):
        """Получение одной привычки по её ID."""
        return db.query(Habit).filter(Habit.id == habit_id).first()

    @staticmethod
    def mark_completed(db: Session, habit_id: int):
        """Отметка привычки как выполненной за сегодня."""
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit or not habit.is_active:
            return habit

        today = date.today()

        if habit.last_completed == today:
            return habit

        if habit.last_updated and habit.last_updated < today - timedelta(days=1):
            habit.days_completed = 0

        habit.days_completed += 1
        habit.last_completed = today
        habit.last_updated = today

        HabitService._create_log(db, habit_id, True)

        if habit.days_completed >= habit.max_days:
            habit.is_active = False
            habit.completed_at = datetime.now()

        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def mark_skipped(db: Session, habit_id: int):
        """Отметка пропуска выполнения привычки."""
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit or not habit.is_active:
            return habit

        habit.days_completed = 0
        habit.last_updated = date.today()
        habit.last_completed = None

        HabitService._create_log(db, habit_id, False)

        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def complete_early(db: Session, habit_id: int):
        """Досрочное завершение привычки до достижения 21 дня."""
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit or not habit.is_active:
            return habit

        habit.is_active = False
        habit.completed_at = datetime.now()
        habit.completed_early = True
        habit.days_completed = max(habit.days_completed, habit.max_days)

        db.commit()
        db.refresh(habit)
        return habit

    @staticmethod
    def _create_log(db: Session, habit_id: int, completed: bool):
        """Внутренний метод для создания или обновления лога выполнения."""
        today = date.today()
        existing = db.query(HabitLog).filter(HabitLog.habit_id == habit_id, HabitLog.date == today).first()

        if existing:
            existing.completed = completed
        else:
            log = HabitLog(habit_id=habit_id, date=today, completed=completed)
            db.add(log)
        db.commit()

    @staticmethod
    def check_21_days(db: Session):
        """Проверка всех активных привычек на соответствие правилу 21 дня."""

        today = date.today()
        habits = db.query(Habit).filter(Habit.is_active == True).all()  # pylint: disable=singleton-comparison

        updated_count = 0
        completed_count = 0

        for habit in habits:
            if habit.last_updated and habit.last_updated < today:
                if habit.last_updated < today - timedelta(days=1):
                    habit.days_completed = 0
                    updated_count += 1
                habit.last_updated = today

            if habit.days_completed >= habit.max_days:
                habit.is_active = False
                habit.completed_at = datetime.now()
                completed_count += 1

        db.commit()
        return {"updated": updated_count, "completed": completed_count}
