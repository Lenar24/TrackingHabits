"""
Модуль является центральной точкой входа для всех Pydantic схем.
"""

from .auth import LoginRequest, RefreshTokenRequest, TokenData, TokenResponse
from .common import ErrorResponse, MessageResponse, PaginatedResponse
from .habit import (
    HabitBase,
    HabitCreate,
    HabitHistoryItem,
    HabitHistoryResponse,
    HabitProgressResponse,
    HabitResponse,
    HabitStreakResponse,
    HabitUpdate,
)
from .habit_log import HabitLogBase, HabitLogResponse
from .stats import DailyLog, HabitStats, OverallStats
from .user import UserBase, UserCreate, UserResponse, UserUpdate, UserWithHabits

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
