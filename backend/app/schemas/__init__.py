"""
Модуль является центральной точкой входа для всех Pydantic схем.
"""

from .common import MessageResponse, ErrorResponse, PaginatedResponse
from .auth import LoginRequest, TokenResponse, TokenData, RefreshTokenRequest
from .user import UserBase, UserCreate, UserUpdate, UserResponse, UserWithHabits
from .habit import (
    HabitBase,
    HabitCreate,
    HabitUpdate,
    HabitResponse,
    HabitProgressResponse,
    HabitStreakResponse,
    HabitHistoryResponse,
    HabitHistoryItem,
)
from .habit_log import HabitLogBase, HabitLogResponse
from .stats import DailyLog, HabitStats, OverallStats

__all__ = [
    # Common
    "MessageResponse",
    "ErrorResponse",
    "PaginatedResponse",
    # Auth
    "LoginRequest",
    "RefreshTokenRequest",
    "TokenResponse",
    "TokenData",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserWithHabits",
    # Habit
    "HabitBase",
    "HabitCreate",
    "HabitUpdate",
    "HabitResponse",
    "HabitProgressResponse",
    "HabitStreakResponse",
    "HabitHistoryResponse",
    "HabitHistoryItem",
    # HabitLog
    "HabitLogBase",
    "HabitLogResponse",
    # Stats
    "DailyLog",
    "HabitStats",
    "OverallStats",
]
