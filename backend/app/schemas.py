from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None


class HabitCreate(HabitBase):
    user_id: int


class Habit(HabitBase):
    id: int
    user_id: int
    created_at: datetime
    is_active: bool
    days_completed: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_id: int
    username: Optional[str] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime
    habits: List[Habit] = []

    class Config:
        from_attributes = True
