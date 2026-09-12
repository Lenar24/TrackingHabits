"""
Модель Habit представляет привычку пользователя.
"""

from typing import Optional, List, TYPE_CHECKING
from datetime import date, datetime, timezone, timedelta
from sqlalchemy import Integer, String, Boolean, Date, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

from .base import BaseModel

if TYPE_CHECKING:
    from .user import User
    from .habit_log import HabitLog


class Habit(BaseModel):
    """
    Модель привычки пользователя.

    Таблица: habits

    Константы:
        MAX_DAYS_DEFAULT: 21 - классический метод 21 дня
        MIN_DAYS: 1 - минимальное количество дней
        MAX_DAYS_LIMIT: 365 - максимум 1 год
        MIN_DAYS_FOR_EARLY_COMPLETE: 7 - минимум дней для досрочного завершения
        MAX_NAME_LENGTH: 255 - максимальная длина названия
        MAX_DESCRIPTION_LENGTH: 1000 - максимальная длина описания
    """

    __tablename__ = "habits"

    # КОНСТАНТЫ
    MAX_DAYS_DEFAULT = 21
    MIN_DAYS = 1
    MAX_DAYS_LIMIT = 365
    MIN_DAYS_FOR_EARLY_COMPLETE = 7
    MAX_NAME_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 1000

    #  ПОЛЯ

    # Внешние ключи
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Основная информация
    name: Mapped[str] = mapped_column(
        String(MAX_NAME_LENGTH),
        nullable=False,
        index=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    # Статус
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True
    )
    completed_early: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    # Прогресс
    days_completed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    max_days: Mapped[int] = mapped_column(
        Integer,
        default=MAX_DAYS_DEFAULT,
        nullable=False
    )

    # Даты
    last_completed: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True
    )

    #  СВЯЗИ

    user: Mapped["User"] = relationship(
        "User",
        back_populates="habits"
    )
    logs: Mapped[List["HabitLog"]] = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    #  ИНДЕКСЫ

    __table_args__ = (
        Index('ix_habits_user_active', 'user_id', 'is_active'),
    )

    #  ВАЛИДАЦИЯ

    @validates('name')
    def validate_name(self, key: str, value: str) -> str:
        """
        Валидация названия привычки.

        Args:
            key: Имя поля (name)
            value: Значение для валидации

        Returns:
            str: Очищенное значение

        Raises:
            ValueError: Если название невалидно
        """
        if not value or not value.strip():
            raise ValueError("Название привычки не может быть пустым")

        if len(value) > self.MAX_NAME_LENGTH:
            raise ValueError(
                f"Название привычки не может превышать {self.MAX_NAME_LENGTH} символов"
            )

        return value.strip()

    @validates('description')
    def validate_description(self, key: str, value: Optional[str]) -> Optional[str]:
        """
        Валидация описания привычки.

        Args:
            key: Имя поля (description)
            value: Значение для валидации

        Returns:
            Optional[str]: Очищенное значение или None

        Raises:
            ValueError: Если описание слишком длинное
        """
        if value is not None:
            if len(value) > self.MAX_DESCRIPTION_LENGTH:
                raise ValueError(
                    f"Описание не может превышать {self.MAX_DESCRIPTION_LENGTH} символов"
                )
            return value.strip()
        return value

    @validates('max_days')
    def validate_max_days(self, key: str, value: int) -> int:
        """
        Валидация количества дней.

        Args:
            key: Имя поля (max_days)
            value: Значение для валидации

        Returns:
            int: Валидное значение

        Raises:
            ValueError: Если количество дней вне допустимого диапазона
        """
        if value < self.MIN_DAYS:
            raise ValueError(
                f"max_days должен быть не менее {self.MIN_DAYS}"
            )

        if value > self.MAX_DAYS_LIMIT:
            raise ValueError(
                f"max_days не может превышать {self.MAX_DAYS_LIMIT}"
            )

        return value

    #  СВОЙСТВА

    @property
    def progress_percentage(self) -> float:
        """
        Процент выполнения привычки.

        Returns:
            float: Процент от 0 до 100
        """
        if self.max_days <= 0:
            return 0.0
        return min(100.0, (self.days_completed / self.max_days) * 100)

    @property
    def is_completed(self) -> bool:
        """
        Завершена ли привычка.

        Returns:
            bool: True если завершена
        """
        return self.days_completed >= self.max_days or self.completed_early

    @property
    def remaining_days(self) -> int:
        """
        Осталось дней до завершения.

        Returns:
            int: Количество оставшихся дней
        """
        return max(0, self.max_days - self.days_completed)

    @property
    def can_complete_early(self) -> bool:
        """
        Можно ли завершить досрочно.

        Returns:
            bool: True если можно завершить досрочно
        """
        return (
            self.is_active and
            self.days_completed >= self.MIN_DAYS_FOR_EARLY_COMPLETE
        )

    @property
    def is_today_completed(self) -> bool:
        """
        Выполнена ли привычка сегодня.

        Returns:
            bool: True если выполнена сегодня
        """
        return self.last_completed == date.today()

    @property
    def days_since_last_completed(self) -> Optional[int]:
        """
        Дней с последнего выполнения.

        Returns:
            Optional[int]: Количество дней или None если никогда не выполнялась
        """
        if not self.last_completed:
            return None
        return (date.today() - self.last_completed).days

    @property
    def status_display(self) -> str:
        """
        Отображение статуса привычки для UI.

        Returns:
            str: Статус на русском языке
        """
        if self.completed_early:
            return "✅ Досрочно завершена"
        if self.is_completed:
            return "✅ Завершена"
        if not self.is_active:
            return "⏸️ Неактивна"
        if self.is_today_completed:
            return "✅ Выполнена сегодня"
        if self.last_completed:
            return f"⏳ Выполнена {self.days_since_last_completed} дн. назад"
        return "📝 Не начиналась"

    #  МЕТОДЫ БИЗНЕС-ЛОГИКИ

    def complete_today(self) -> dict:
        """
        Отметить выполнение привычки за сегодня.

        Returns:
            dict: Результат операции
                - success: bool
                - message: str
                - habit: Habit
                - completed: bool (достигнута ли цель)
                - progress: str (прогресс в формате "X/Y")
                - already_completed: bool (была ли уже выполнена)
        """
        if not self.is_active:
            return {
                "success": False,
                "message": "Привычка уже завершена",
                "habit": self
            }

        today = date.today()

        if self.last_completed == today:
            return {
                "success": False,
                "message": "Привычка уже выполнена сегодня",
                "habit": self,
                "already_completed": True
            }

        # Проверка пропуска дней
        if self.last_completed:
            days_since_last = (today - self.last_completed).days
            if days_since_last > 1:
                # Сброс прогресса при длительном пропуске
                self.days_completed = 0

        # Увеличиваем прогресс
        self.days_completed += 1
        self.last_completed = today

        # Проверка достижения цели
        completed = False
        if self.days_completed >= self.max_days:
            self.is_active = False
            self.completed_at = datetime.now(timezone.utc)
            completed = True

        return {
            "success": True,
            "message": "Привычка выполнена",
            "habit": self,
            "completed": completed,
            "progress": f"{self.days_completed}/{self.max_days}",
            "already_completed": False
        }

    def skip_today(self) -> dict:
        """Пропустить выполнение привычки за сегодня."""
        from datetime import date

        if not self.is_active:
            return {
                "success": False,
                "message": "Привычка уже завершена",
                "habit": self
            }

        today = date.today()

        if self.last_completed == today:
            return {
                "success": False,
                "message": "Нельзя пропустить уже выполненную привычку",
                "habit": self
            }

        # ✅ СБРОС ПРОГРЕССА ВСЕГДА при пропуске
        self.days_completed = 0
        self.last_completed = None

        return {
            "success": True,
            "message": "Привычка пропущена",
            "habit": self,
            "progress": f"{self.days_completed}/{self.max_days}"
        }

    def complete_early(self) -> dict:
        """
        Досрочное завершение привычки.

        Returns:
            dict: Результат операции
                - success: bool
                - message: str
                - habit: Habit
                - required_days: int (минимальное количество дней)
                - current_days: int (текущее количество дней)
        """
        if not self.is_active:
            return {
                "success": False,
                "message": "Привычка уже завершена",
                "habit": self
            }

        if self.days_completed < self.MIN_DAYS_FOR_EARLY_COMPLETE:
            return {
                "success": False,
                "message": (
                    f"Нельзя завершить досрочно. "
                    f"Минимум {self.MIN_DAYS_FOR_EARLY_COMPLETE} дней, "
                    f"выполнено {self.days_completed}"
                ),
                "habit": self,
                "required_days": self.MIN_DAYS_FOR_EARLY_COMPLETE,
                "current_days": self.days_completed
            }

        self.is_active = False
        self.completed_early = True
        self.completed_at = datetime.now(timezone.utc)

        return {
            "success": True,
            "message": "Привычка досрочно завершена",
            "habit": self,
            "days_completed": self.days_completed
        }

    def reset(self) -> dict:
        """
        Сброс прогресса привычки.

        Returns:
            dict: Результат операции
                - success: bool
                - message: str
                - habit: Habit
        """
        if not self.is_active:
            return {
                "success": False,
                "message": "Нельзя сбросить завершенную привычку",
                "habit": self
            }

        self.days_completed = 0
        self.last_completed = None
        self.completed_early = False

        return {
            "success": True,
            "message": "Прогресс сброшен",
            "habit": self
        }

    def activate(self) -> dict:
        """
        Активация привычки (если она была завершена).

        Returns:
            dict: Результат операции
                - success: bool
                - message: str
                - habit: Habit
        """
        if self.is_active:
            return {
                "success": False,
                "message": "Привычка уже активна",
                "habit": self
            }

        self.is_active = True
        self.completed_at = None
        self.completed_early = False

        return {
            "success": True,
            "message": "Привычка активирована",
            "habit": self
        }

    def get_streak(self) -> int:
        """
        Получить текущую непрерывную серию (стрик).

        Returns:
            int: Количество дней подряд выполнения
        """
        if not self.last_completed:
            return 0

        today = date.today()
        if self.last_completed != today:
            return 0

        # Считаем стрик из логов
        from .habit_log import HabitLog

        logs = self.logs.filter(
            HabitLog.completed == True
        ).order_by(HabitLog.date.desc()).limit(365).all()

        streak = 0
        for log in logs:
            if log.date == today - timedelta(days=streak):
                streak += 1
            else:
                break

        return streak

    # СТАТИЧЕСКИЕ МЕТОДЫ

    @staticmethod
    def get_default_max_days() -> int:
        """Получить значение по умолчанию для max_days."""
        return Habit.MAX_DAYS_DEFAULT

    @staticmethod
    def validate_name_static(name: str) -> bool:
        """
        Статическая валидация имени (для использования без объекта).

        Args:
            name: Название привычки

        Returns:
            bool: True если валидно
        """
        return bool(name and name.strip() and len(name) <= Habit.MAX_NAME_LENGTH)

    #  МАГИЧЕСКИЕ МЕТОДЫ

    def __repr__(self) -> str:
        return f"<Habit id={self.id} name={self.name} user_id={self.user_id}>"

    def __str__(self) -> str:
        return f"{self.name} ({self.days_completed}/{self.max_days})"
