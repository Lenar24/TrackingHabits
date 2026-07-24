from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager  # <-- Добавляем импорт

from . import models, schemas, crud
from .database import engine, get_db
from .scheduler import start_scheduler, test_reminder

load_dotenv()

models.Base.metadata.create_all(bind=engine)

# LIFESPAN

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Код при СТАРТЕ ---
    print("🚀 Запуск приложения...")
    scheduler = start_scheduler()
    app.state.scheduler = scheduler  # Сохраняем планировщик в app.state
    print("✅ Планировщик напоминаний запущен!")

    yield  # <-- Здесь приложение работает

    # --- Код при ОСТАНОВКЕ ---
    print("🛑 Остановка приложения...")
    if hasattr(app.state, 'scheduler') and app.state.scheduler:
        app.state.scheduler.shutdown()
        print("🛑 Планировщик остановлен")

# СОЗДАНИЕ ПРИЛОЖЕНИЯ С LIFESPAN

app = FastAPI(title="Habit Tracker API", lifespan=lifespan)

# ЭНДПОИНТЫ

@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    """Получить всех пользователей"""
    users = db.query(models.User).all()
    return users


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, есть ли пользователь
    existing_user = crud.get_user(db, user_id=user.user_id)
    if existing_user:
        # Если пользователь есть, но chat_id изменился — обновляем
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


@app.post("/habits/", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(get_db)):
    return crud.create_habit(db=db, habit=habit)


@app.get("/habits/{user_id}", response_model=List[schemas.Habit])
def get_habits(user_id: int, db: Session = Depends(get_db)):
    return crud.get_habits(db, user_id=user_id)


@app.put("/habits/{habit_id}/complete")
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    return crud.complete_habit(db, habit_id)


@app.post("/reminders/test")
async def test_reminders():
    """Тестовый эндпоинт для отправки напоминаний вручную"""
    from .scheduler import send_daily_reminders
    await send_daily_reminders()
    return {"message": "Напоминания отправлены"}


@app.put("/users/{user_id}/chat_id")
def update_chat_id(user_id: int, payload: dict, db: Session = Depends(get_db)):
    chat_id = payload.get("chat_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    user = crud.update_user_chat_id(db, user_id, chat_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
