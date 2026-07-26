from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
from . import models, schemas


# ПОЛЬЗОВАТЕЛИ

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        user_id=user.user_id,
        chat_id=user.chat_id,
        username=user.username
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_chat_id(db: Session, user_id: int, chat_id: int):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user:
        user.chat_id = chat_id
        db.commit()
        db.refresh(user)
    return user


# ПРИВЫЧКИ

def create_habit(db: Session, habit: schemas.HabitCreate):
    db_habit = models.Habit(
        user_id=habit.user_id,
        name=habit.name,
        description=habit.description,
        last_updated=date.today()
    )
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def get_habits(db: Session, user_id: int, active_only: bool = True):
    query = db.query(models.Habit).filter(models.Habit.user_id == user_id)
    if active_only:
        query = query.filter(models.Habit.is_active == True)
    return query.all()


def get_habit(db: Session, habit_id: int):
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()


def update_habit(db: Session, habit_id: int, habit_update: schemas.HabitUpdate):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None

    if habit_update.name is not None:
        habit.name = habit_update.name
    if habit_update.description is not None:
        habit.description = habit_update.description
    if habit_update.is_active is not None:
        habit.is_active = habit_update.is_active

    db.commit()
    db.refresh(habit)
    return habit


def delete_habit(db: Session, habit_id: int):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        db.delete(habit)
        db.commit()
        return True
    return False


# ПРОГРЕСС ПРИВЫЧЕК

def mark_habit_completed(db: Session, habit_id: int):
    """Отметить привычку как выполненную сегодня"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None

    today = date.today()

    # Если уже выполнена сегодня — пропускаем
    if habit.last_completed == today:
        return habit

    # Если был пропуск (не обновлялась вчера) — сбрасываем счётчик
    if habit.last_updated and habit.last_updated < today - timedelta(days=1):
        habit.days_completed = 0

    # Увеличиваем счётчик
    habit.days_completed += 1
    habit.last_completed = today
    habit.last_updated = today

    # Проверяем, достигнут ли 21 день
    if habit.days_completed >= habit.max_days:
        habit.is_active = False
        habit.completed_at = datetime.now()

    db.commit()
    db.refresh(habit)
    return habit


def mark_habit_skipped(db: Session, habit_id: int):
    """Отметить привычку как пропущенную (сброс счётчика)"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None

    habit.days_completed = 0
    habit.last_updated = date.today()

    db.commit()
    db.refresh(habit)
    return habit


def complete_habit_early(db: Session, habit_id: int):
    """Ручное завершение привычки (пользователь считает, что привычка сформирована)"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None

    if not habit.is_active:
        return habit

    habit.is_active = False
    habit.completed_at = datetime.now()
    # Устанавливаем days_completed = max_days, если ещё не достигнут
    if habit.days_completed < habit.max_days:
        habit.days_completed = habit.max_days

    db.commit()
    db.refresh(habit)
    return habit


def check_and_update_habits(db: Session):
    """
    Проверяет все активные привычки по правилу 21 дня.
    Автоматически завершает привычки с days_completed >= 21.
    Сбрасывает счётчик для привычек, которые не обновлялись > 1 дня.
    """
    today = date.today()
    habits = db.query(models.Habit).filter(models.Habit.is_active == True).all()

    updated_count = 0
    completed_count = 0

    for habit in habits:
        # Если привычка не обновлялась сегодня
        if habit.last_updated and habit.last_updated < today:
            # Если последнее обновление было вчера или позже
            if habit.last_updated < today - timedelta(days=1):
                # Пропущен день — сбрасываем счётчик
                habit.days_completed = 0
                updated_count += 1
            habit.last_updated = today

        # Проверяем правило 21 дня
        if habit.days_completed >= habit.max_days:
            habit.is_active = False
            habit.completed_at = datetime.now()
            completed_count += 1

    db.commit()
    return {
        "updated": updated_count,
        "completed": completed_count
    }
