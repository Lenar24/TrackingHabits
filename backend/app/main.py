from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .api import habits_router, reminders_router, stats_router, users_router
from .scheduler import start_scheduler
from .services.habit_service import HabitService
from .utils.database import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Запуск приложения...")
    scheduler = start_scheduler()
    app.state.scheduler = scheduler
    print("✅ Планировщик напоминаний запущен!")
    yield
    print("🛑 Остановка приложения...")
    if hasattr(app.state, "scheduler") and app.state.scheduler:
        app.state.scheduler.shutdown()
        print("🛑 Планировщик остановлен")


app = FastAPI(title="Habit Tracker API", lifespan=lifespan)

# Подключение роутеров
app.include_router(habits_router)
app.include_router(users_router)
app.include_router(stats_router)
app.include_router(reminders_router)


@app.get("/")
def read_root():
    return {"message": "Habit Tracker API is running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/habits/check-21-days")
def check_21_days(db: Session = Depends(get_db)):  # <-- Правильно!
    result = HabitService.check_21_days(db)
    return result
