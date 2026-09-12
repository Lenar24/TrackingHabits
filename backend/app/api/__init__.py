"""
Модуль служит точкой входа для всех API роутеров приложения.
"""

from .auth import router as auth_router
from .habits import router as habits_router
from .users import router as users_router
from .stats import router as stats_router
from .reminders import router as reminders_router
from .dependencies import get_habit_or_404, get_active_habit

__all__ = [
    "auth_router",
    "habits_router",
    "users_router",
    "stats_router",
    "reminders_router",
    "get_habit_or_404",
    "get_active_habit",
]
