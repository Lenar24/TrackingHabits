"""
Pydantic схемы для логов привычек.
"""

from datetime import date
from pydantic import BaseModel, ConfigDict


class HabitLogBase(BaseModel):
    """Базовая схема лога привычки."""
    habit_id: int
    date: date
    completed: bool


class HabitLogResponse(HabitLogBase):
    """Полная схема лога для ответа."""
    id: int

    model_config = ConfigDict(from_attributes=True)
