from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from . import models, schemas, crud
from .database import engine, get_db
from .scheduler import start_scheduler

load_dotenv()

models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Запуск приложения...")
    scheduler = start_scheduler()
    app.state.scheduler = scheduler
    print("✅ Планировщик напоминаний запущен!")

    yield

    print("🛑 Остановка приложения...")
    if hasattr(app.state, 'scheduler') and app.state.scheduler:
        app.state.scheduler.shutdown()
        print("🛑 Планировщик остановлен")


app = FastAPI(title="Habit Tracker API", lifespan=lifespan)


# ЭНДПОИНТЫ ПОЛЬЗОВАТЕЛЕЙ

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user(db, user_id=user.user_id)
    if existing_user:
        if existing_user.chat_id != user.chat_id:
            existing_user = crud.update_user_chat_id(db, user.user_id, user.chat_id)
        return existing_user
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}/chat_id")
def update_chat_id(user_id: int, payload: dict, db: Session = Depends(get_db)):
    chat_id = payload.get("chat_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    user = crud.update_user_chat_id(db, user_id, chat_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ЭНДПОИНТЫ ПРИВЫЧЕК

@app.post("/habits/", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.create_habit(db=db, habit=habit)


@app.get("/habits/{user_id}", response_model=List[schemas.Habit])
def get_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_habits(db, user_id=user_id)


@app.get("/habits/{user_id}/all", response_model=List[schemas.Habit])
def get_all_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_habits(db, user_id=user_id, active_only=False)


@app.get("/habits/item/{habit_id}", response_model=schemas.Habit)
def get_habit_by_id(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.put("/habits/{habit_id}", response_model=schemas.Habit)
def update_habit(habit_id: int, habit_update: schemas.HabitUpdate, db: Session = Depends(get_db)):
    habit = crud.update_habit(db, habit_id, habit_update)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.delete("/habits/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    if not crud.delete_habit(db, habit_id):
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted"}


# ЭНДПОИНТЫ ПРОГРЕССА

@app.post("/habits/{habit_id}/complete")
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.mark_habit_completed(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.post("/habits/{habit_id}/skip")
def skip_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.mark_habit_skipped(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.post("/habits/{habit_id}/complete-early")
def complete_habit_early(habit_id: int, db: Session = Depends(get_db)):
    habit = crud.complete_habit_early(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@app.post("/habits/check-21-days")
def check_21_days_rule(db: Session = Depends(get_db)):
    result = crud.check_and_update_habits(db)
    return result


# ЭНДПОИНТ СТАТИСТИКИ

@app.get("/habits/{user_id}/stats")
def get_habit_stats(user_id: int, db: Session = Depends(get_db)):
    """Получить статистику по всем привычкам пользователя"""
    return crud.get_habit_stats(db, user_id)


# ЭНДПОИНТЫ НАПОМИНАНИЙ

@app.post("/reminders/test")
async def test_reminders():
    from .scheduler import send_daily_reminders
    await send_daily_reminders()
    return {"message": "Напоминания отправлены"}
