"""
Pydantic схемы для статистики.
"""

from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel


class DailyLog(BaseModel):
    """Ежедневный лог для статистики."""
    date: date
    completed: bool


class HabitStats(BaseModel):
    """Статистика по привычке."""
    habit_id: int
    name: str
    is_active: bool
    days_completed: int
    max_days: int
    progress_percentage: float
    total_logs: int
    completed_logs: int
    best_streak: int
    current_streak: int
    last_7_days: List[DailyLog]
    completed_at: Optional[datetime]
    created_at: datetime


class OverallStats(BaseModel):
    """Общая статистика пользователя."""
    total_habits: int
    active_habits: int
    completed_habits: int
    total_days_completed: int
    best_overall_streak: int
    completion_rate: float
