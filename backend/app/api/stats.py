"""
Модуль предоставляет эндпоинты для получения статистики.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models import HabitLog, Habit
from ..schemas import HabitStats, OverallStats
from ..services import HabitService
from ..utils.database import get_db
from ..utils.auth import get_current_user
from ..models import User
from .dependencies import get_habit_or_404

router = APIRouter()


@router.get("/overall", response_model=OverallStats)
def get_overall_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получение общей статистики по всем привычкам пользователя.
    """
    habits = HabitService.get_habits(db, current_user.id, active_only=False)

    total_habits = len(habits)
    active_habits = sum(1 for h in habits if h.is_active)
    completed_habits = total_habits - active_habits
    total_days_completed = sum(h.days_completed for h in habits)

    # Расчет лучшей серии
    best_streak = 0
    for habit in habits:
        stats = HabitService.get_habit_stats(db, habit.id)
        if stats["best_streak"] > best_streak:
            best_streak = stats["best_streak"]

    # Коэффициент выполнения
    completion_rate = 0
    if total_habits > 0:
        total_completed = sum(1 for h in habits if h.is_completed)
        completion_rate = (total_completed / total_habits) * 100

    return OverallStats(
        total_habits=total_habits,
        active_habits=active_habits,
        completed_habits=completed_habits,
        total_days_completed=total_days_completed,
        best_overall_streak=best_streak,
        completion_rate=round(completion_rate, 2)
    )


@router.get("/habits/{habit_id}", response_model=HabitStats)
def get_habit_stats(
    habit: Habit = Depends(get_habit_or_404),  # ✅ Проверка прав
    db: Session = Depends(get_db),
):
    """
    Получение детальной статистики по конкретной привычке.
    """
    return HabitService.get_habit_stats(db, habit.id)


@router.get("/habits/{habit_id}/progress")
def get_habit_progress(
    habit: Habit = Depends(get_habit_or_404),  # ✅ Проверка прав
):
    """
    Получение прогресса выполнения привычки.
    """
    return {
        "habit_id": habit.id,
        "name": habit.name,
        "days_completed": habit.days_completed,
        "max_days": habit.max_days,
        "progress_percentage": habit.progress_percentage,
        "is_completed": habit.is_completed,
        "is_active": habit.is_active,
        "remaining_days": max(0, habit.max_days - habit.days_completed),
    }


@router.get("/habits/{habit_id}/history")
def get_habit_history(
    habit: Habit = Depends(get_habit_or_404),  # ✅ Проверка прав
    limit: int = 30,
):
    """
    Получение истории выполнения привычки за последние N дней.
    """
    logs = habit.logs.order_by(HabitLog.date.desc()).limit(limit).all()

    return {
        "habit_id": habit.id,
        "name": habit.name,
        "logs": [
            {
                "date": log.date,
                "completed": log.completed
            }
            for log in logs
        ]
    }
