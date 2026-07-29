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

    # 🔥 Если привычка уже завершена — возвращаем без изменений
    if not habit.is_active:
        return habit

    today = date.today()

    if habit.last_completed == today:
        return habit

    if habit.last_updated and habit.last_updated < today - timedelta(days=1):
        habit.days_completed = 0

    habit.days_completed += 1
    habit.last_completed = today
    habit.last_updated = today

    create_habit_log(db, habit_id, completed=True)

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

    # 🔥 Если привычка уже завершена — возвращаем без изменений
    if not habit.is_active:
        return habit

    today = date.today()

    habit.days_completed = 0
    habit.last_updated = today
    habit.last_completed = None

    create_habit_log(db, habit_id, completed=False)

    db.commit()
    db.refresh(habit)
    return habit


def complete_habit_early(db: Session, habit_id: int):
    """Ручное завершение привычки (досрочно)"""
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None

    if not habit.is_active:
        return habit

    habit.is_active = False
    habit.completed_at = datetime.now()
    habit.completed_early = True  # <-- Помечаем, что завершена досрочно
    if habit.days_completed < habit.max_days:
        habit.days_completed = habit.max_days

    db.commit()
    db.refresh(habit)
    return habit


def check_and_update_habits(db: Session):
    """Проверка правила 21 дня"""
    today = date.today()
    habits = db.query(models.Habit).filter(models.Habit.is_active == True).all()

    updated_count = 0
    completed_count = 0

    for habit in habits:
        if habit.last_updated and habit.last_updated < today:
            if habit.last_updated < today - timedelta(days=1):
                habit.days_completed = 0
                create_habit_log(db, habit.id, completed=False)
                updated_count += 1
            habit.last_updated = today

        if habit.days_completed >= habit.max_days:
            habit.is_active = False
            habit.completed_at = datetime.now()
            habit.completed_early = False  # <-- Завершена через 21 день (не досрочно)
            completed_count += 1

    db.commit()
    return {"updated": updated_count, "completed": completed_count}


# ЛОГИ ПРИВЫЧЕК

def create_habit_log(db: Session, habit_id: int, completed: bool = True):
    """Создаёт запись о выполнении/пропуске привычки"""
    today = date.today()

    existing = db.query(models.HabitLog).filter(
        models.HabitLog.habit_id == habit_id,
        models.HabitLog.date == today
    ).first()

    if existing:
        existing.completed = completed
        db.commit()
        db.refresh(existing)
        return existing

    log = models.HabitLog(
        habit_id=habit_id,
        date=today,
        completed=completed
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_habit_stats(db: Session, user_id: int):
    """Получает статистику по всем привычкам пользователя"""
    habits = db.query(models.Habit).filter(models.Habit.user_id == user_id).all()

    result = []
    for habit in habits:
        logs = db.query(models.HabitLog).filter(
            models.HabitLog.habit_id == habit.id
        ).order_by(models.HabitLog.date.desc()).limit(30).all()

        total_days = len(logs)
        completed_days = sum(1 for log in logs if log.completed)

        last_7_days = []
        for log in logs[:7]:
            last_7_days.append({
                "date": log.date.strftime("%d.%m"),
                "completed": log.completed
            })

        best_streak = 0
        current_streak = 0
        for log in sorted(logs, key=lambda x: x.date):
            if log.completed:
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0

        result.append({
            "id": habit.id,
            "name": habit.name,
            "is_active": habit.is_active,
            "days_completed": habit.days_completed,
            "max_days": habit.max_days,
            "completed_at": habit.completed_at,
            "created_at": habit.created_at,
            "total_logs": total_days,
            "completed_logs": completed_days,
            "best_streak": best_streak,
            "last_7_days": last_7_days
        })

    return result
