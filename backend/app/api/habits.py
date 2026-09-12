"""
Модуль предоставляет эндпоинты для управления привычками пользователей.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..schemas import HabitCreate, HabitUpdate, HabitResponse, MessageResponse
from ..services import HabitService
from ..utils.database import get_db
from ..utils.auth import get_current_user
from ..models import User, Habit
from .dependencies import get_habit_or_404, get_active_habit

router = APIRouter()


# ============ CRUD ОПЕРАЦИИ ============

@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(
    habit_data: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создание новой привычки для текущего пользователя.
    """
    try:
        habit = HabitService.create_habit(db, current_user.id, habit_data)
        return habit
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[HabitResponse])
def get_habits(
    active_only: bool = Query(True, description="Только активные привычки"),
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(100, ge=1, le=1000, description="Лимит записей"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получение списка привычек текущего пользователя.
    """
    habits = HabitService.get_habits(
        db,
        current_user.id,
        active_only=active_only,
        skip=skip,
        limit=limit
    )
    return habits


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(
    habit: Habit = Depends(get_habit_or_404)
):
    """
    Получение конкретной привычки по её ID.
    """
    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(
    habit_update: HabitUpdate,
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
):
    """
    Обновление данных привычки.
    """
    try:
        updated = HabitService.update_habit(db, habit.id, habit_update)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit not found"
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{habit_id}", response_model=MessageResponse)
def delete_habit(
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
):
    """
    Удаление привычки.
    """
    success = HabitService.delete_habit(db, habit.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )
    return MessageResponse(message="Habit deleted successfully")


# ============ ДЕЙСТВИЯ С ПРИВЫЧКОЙ ============

@router.post("/{habit_id}/complete")
def complete_habit(
    habit: Habit = Depends(get_active_habit),
    db: Session = Depends(get_db),
):
    """
    Отметка привычки как выполненной за сегодня.
    """
    try:
        result = HabitService.mark_completed(db, habit.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{habit_id}/skip")
def skip_habit(
    habit: Habit = Depends(get_active_habit),
    db: Session = Depends(get_db),
):
    """
    Отметка пропуска выполнения привычки на сегодня.
    """
    try:
        result = HabitService.mark_skipped(db, habit.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{habit_id}/complete-early")
def complete_habit_early(
    habit: Habit = Depends(get_active_habit),
    db: Session = Depends(get_db),
):
    """
    Досрочное завершение привычки до достижения 21 дня.
    """
    try:
        result = HabitService.complete_early(db, habit.id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ============ ДОПОЛНИТЕЛЬНЫЕ ЭНДПОИНТЫ ============

@router.get("/{habit_id}/progress")
def get_habit_progress(
    habit: Habit = Depends(get_habit_or_404),
):
    """
    Получение прогресса выполнения привычки.
    """
    return {
        "habit_id": habit.id,
        "name": habit.name,
        "progress_percentage": habit.progress_percentage,
        "remaining_days": habit.remaining_days,
        "is_completed": habit.is_completed,
        "is_active": habit.is_active,
        "can_complete_early": habit.can_complete_early,
        "is_today_completed": habit.is_today_completed,
        "days_since_last": habit.days_since_last_completed,
        "status_display": habit.status_display,
        "max_days": habit.max_days,
        "days_completed": habit.days_completed,
    }


@router.get("/{habit_id}/streak")
def get_habit_streak(
    habit: Habit = Depends(get_habit_or_404),
):
    """
    Получение текущей серии (стрика) привычки.
    """
    return {
        "habit_id": habit.id,
        "name": habit.name,
        "streak": habit.get_streak(),
        "last_completed": habit.last_completed,
        "is_today_completed": habit.is_today_completed,
    }


@router.post("/{habit_id}/reset", response_model=MessageResponse)
def reset_habit(
    habit: Habit = Depends(get_active_habit),
    db: Session = Depends(get_db),
):
    """
    Сброс прогресса привычки.
    """
    result = habit.reset()

    if result["success"]:
        db.commit()
        db.refresh(habit)
        return MessageResponse(message=result["message"])

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=result["message"]
    )


@router.post("/{habit_id}/activate", response_model=MessageResponse)
def activate_habit(
    habit: Habit = Depends(get_habit_or_404),
    db: Session = Depends(get_db),
):
    """
    Активация завершенной привычки.
    """
    result = habit.activate()

    if result["success"]:
        db.commit()
        db.refresh(habit)
        return MessageResponse(message=result["message"])

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=result["message"]
    )


@router.post("/check-21-days")
def check_21_days_rule(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ручной запуск проверки привычек на достижение 21 дня.
    """
    result = HabitService.check_21_days(db, current_user.id)
    return result
