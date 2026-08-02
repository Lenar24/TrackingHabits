from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .habit import Habit


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
