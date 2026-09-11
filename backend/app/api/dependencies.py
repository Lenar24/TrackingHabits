"""
Общие зависимости для API эндпоинтов.
"""

from typing import Optional
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.orm import Session

from ..models import Habit, User
from ..services import HabitService
from ..utils.database import get_db
from ..utils.auth import get_current_user, get_current_user_optional


def get_habit_or_404(
        habit_id: int = Path(..., description="ID привычки", ge=1),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Habit:
    """
    Получение привычки по ID с проверкой прав доступа.

    Args:
        habit_id: ID привычки
        db: Сессия БД
        current_user: Текущий пользователь

    Returns:
        Habit: Объект привычки

    Raises:
        HTTPException: 404 если привычка не найдена
        HTTPException: 403 если привычка не принадлежит пользователю
    """
    habit = HabitService.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Habit not found"
        )

    if habit.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this habit"
        )

    return habit


def get_habit_optional(
        habit_id: int = Path(..., description="ID привычки", ge=1),
        db: Session = Depends(get_db),
        current_user: Optional[User] = Depends(get_current_user_optional)
) -> Optional[Habit]:
    """
    Получение привычки по ID без строгой проверки прав.
    Используется для публичных эндпоинтов или админ-доступа.
    """
    habit = HabitService.get_habit(db, habit_id)

    if not habit:
        return None

    # Если пользователь авторизован, проверяем права
    if current_user and habit.user_id != current_user.id:
        return None

    return habit


def get_active_habit(
        habit_id: int = Path(..., description="ID привычки", ge=1),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> Habit:
    """
    Получение активной привычки с проверкой прав.
    """
    habit = get_habit_or_404(habit_id, db, current_user)

    if not habit.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Habit is already completed or inactive"
        )

    return habit
