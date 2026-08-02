from datetime import date
from typing import Optional

from pydantic import BaseModel


class HabitLogBase(BaseModel):
    habit_id: int
    date: date
    completed: bool


class HabitLog(HabitLogBase):
    id: int

    class Config:
        from_attributes = True
