"""
Pydantic схемы для привычек.
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, field_validator


class HabitBase(BaseModel):
    """Базовая схема привычки."""
    name: str = Field(..., min_length=1, max_length=255, description="Название привычки")
    description: Optional[str] = Field(None, max_length=1000, description="Описание")
    max_days: int = Field(21, ge=1, le=365, description="Целевое количество дней")

    @field_validator('name')
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Название привычки не может быть пустым')
        return v.strip()


class HabitCreate(HabitBase):
    """Схема для создания привычки. user_id берется из токена."""
    pass


class HabitUpdate(BaseModel):
    """Схема для обновления привычки."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None
    max_days: Optional[int] = Field(None, ge=1, le=365)

    @field_validator('name')
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v or not v.strip():
                raise ValueError('Название привычки не может быть пустым')
            return v.strip()
        return v


class HabitResponse(BaseModel):
    """Полная схема привычки для ответа."""
    id: int
    user_id: int
    name: str
    description: Optional[str]
    is_active: bool
    completed_early: bool
    days_completed: int
    max_days: int
    created_at: datetime
    updated_at: datetime
    last_completed: Optional[date]
    completed_at: Optional[datetime]

    @property
    def progress_percentage(self) -> float:
        """Процент выполнения."""
        if self.max_days <= 0:
            return 0.0
        return min(100.0, (self.days_completed / self.max_days) * 100)

    @property
    def is_completed(self) -> bool:
        """Завершена ли привычка."""
        return self.days_completed >= self.max_days or self.completed_early

    @property
    def remaining_days(self) -> int:
        """Осталось дней до завершения."""
        return max(0, self.max_days - self.days_completed)

    @property
    def can_complete_early(self) -> bool:
        """Можно ли завершить досрочно."""
        return self.is_active and self.days_completed >= 7

    @property
    def is_today_completed(self) -> bool:
        """Выполнена ли привычка сегодня."""
        return self.last_completed == date.today()

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "properties": {
                "progress_percentage": {
                    "type": "number",
                    "description": "Процент выполнения"
                },
                "is_completed": {
                    "type": "boolean",
                    "description": "Завершена ли привычка"
                },
                "remaining_days": {
                    "type": "integer",
                    "description": "Осталось дней до завершения"
                },
                "can_complete_early": {
                    "type": "boolean",
                    "description": "Можно ли завершить досрочно"
                },
                "is_today_completed": {
                    "type": "boolean",
                    "description": "Выполнена ли привычка сегодня"
                }
            }
        }
    )


class HabitProgressResponse(BaseModel):
    """Прогресс выполнения привычки."""
    habit_id: int
    name: str
    progress_percentage: float
    remaining_days: int
    is_completed: bool
    is_active: bool
    can_complete_early: bool
    is_today_completed: bool
    days_since_last: Optional[int]
    status_display: str
    max_days: int
    days_completed: int

    model_config = ConfigDict(from_attributes=True)


class HabitStreakResponse(BaseModel):
    """Серия выполнения привычки."""
    habit_id: int
    name: str
    streak: int
    last_completed: Optional[date]
    is_today_completed: bool

    model_config = ConfigDict(from_attributes=True)


class HabitHistoryItem(BaseModel):
    """Элемент истории."""
    date: str
    day: str
    completed: bool


class HabitHistoryResponse(BaseModel):
    """История выполнения привычки."""
    habit_id: int
    name: str
    days: int
    history: List[HabitHistoryItem]
    completed_count: int
    completion_rate: float

    model_config = ConfigDict(from_attributes=True)
