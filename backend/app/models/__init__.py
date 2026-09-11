"""
Модуль является центральной точкой входа для всех моделей базы данных.
Он импортирует и экспортирует все модели SQLAlchemy,
обеспечивая единый интерфейс для работы с базой данных.
Упрощает импорт моделей в других частях приложения и улучшает поддерживаемость кода.
"""

from .base import Base
from .user import User
from .habit import Habit
from .habit_log import HabitLog

__all__ = ["Base", "User", "Habit", "HabitLog"]
