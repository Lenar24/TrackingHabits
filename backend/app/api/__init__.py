"""
Модуль служит точкой входа для всех API роутеров приложения.
Он импортирует и экспортирует все роутеры, обеспечивая централизованное
управление маршрутами и упрощая их подключение в главном приложении.
"""

from .habits import router as habits_router
from .reminders import router as reminders_router
from .stats import router as stats_router
from .users import router as users_router

__all__ = ["habits_router", "users_router", "stats_router", "reminders_router"]
