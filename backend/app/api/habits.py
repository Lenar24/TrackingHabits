"""
Модуль предоставляет эндпоинты для управления привычками пользователей.
Включает операции CRUD (создание, чтение, обновление, удаление),
а также специальные методы для отметки выполнения, пропуска и досрочного завершения привычек.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import Habit as HabitSchema
from ..schemas import HabitCreate, HabitUpdate
from ..services import HabitService
from ..utils.database import get_db

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("/", response_model=HabitSchema)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    """Создание новой привычки для пользователя."""
    return HabitService.create_habit(db, habit)


@router.get("/{user_id}", response_model=List[HabitSchema])
def get_habits(user_id: int, db: Session = Depends(get_db)):
    """Получение списка активных привычек пользователя."""
    return HabitService.get_habits(db, user_id)


@router.get("/{user_id}/all", response_model=List[HabitSchema])
def get_all_habits(user_id: int, db: Session = Depends(get_db)):
    """Получение всех привычек пользователя (включая завершенные)."""
    return HabitService.get_habits(db, user_id, active_only=False)


@router.get("/item/{habit_id}", response_model=HabitSchema)
def get_habit_by_id(habit_id: int, db: Session = Depends(get_db)):
    """Получение конкретной привычки по её ID."""
    habit = HabitService.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.put("/{habit_id}", response_model=HabitSchema)
def update_habit(habit_id: int, _habit_update: HabitUpdate, db: Session = Depends(get_db)):
    """Обновление данных привычки."""
    habit = HabitService.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    # Реализовать обновление
    return habit


@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    """Удаление привычки из базы данных."""
    habit = HabitService.get_habit(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted"}


@router.post("/{habit_id}/complete")
def complete_habit(habit_id: int, db: Session = Depends(get_db)):
    """Отметка привычки как выполненной за сегодня."""
    habit = HabitService.mark_completed(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("/{habit_id}/skip")
def skip_habit(habit_id: int, db: Session = Depends(get_db)):
    """Отметка пропуска выполнения привычки на сегодня."""
    habit = HabitService.mark_skipped(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("/{habit_id}/complete-early")
def complete_habit_early(habit_id: int, db: Session = Depends(get_db)):
    """Досрочное завершение привычки до достижения 21 дня."""
    habit = HabitService.complete_early(db, habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("/check-21-days")
def check_21_days_rule(db: Session = Depends(get_db)):
    """Ручной запуск проверки привычек на достижение 21 дня."""
    result = HabitService.check_21_days(db)
    return result
