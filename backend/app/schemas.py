from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List


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
    max_days: int = 21
    last_updated: date
    last_completed: Optional[date] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None


class UserCreate(UserBase):
    chat_id: Optional[int] = None


class User(UserBase):
    id: int
    created_at: datetime
    chat_id: Optional[int] = None
    habits: List[Habit] = []

    class Config:
        from_attributes = True
