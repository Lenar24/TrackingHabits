from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None


class HabitCreate(HabitBase):
    user_id: int


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Habit(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    days_completed: int
    max_days: int
    last_updated: date
    last_completed: Optional[date] = None
    completed_at: Optional[datetime] = None
    completed_early: bool = False

    class Config:
        from_attributes = True
