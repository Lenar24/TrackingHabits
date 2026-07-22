from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(user_id=user.user_id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_habit(db: Session, habit: schemas.HabitCreate):
    db_habit = models.Habit(**habit.model_dump())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_habits(db: Session, user_id: int):
    return db.query(models.Habit).filter(models.Habit.user_id == user_id).all()

def complete_habit(db: Session, habit_id: int):
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if habit:
        habit.days_completed += 1
        db.commit()
        db.refresh(habit)
    return habit
