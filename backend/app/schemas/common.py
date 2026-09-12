"""
Общие Pydantic схемы для API.
"""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar('T')


class MessageResponse(BaseModel):
    """Стандартный ответ с сообщением."""
    message: str
    success: bool = True
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Ответ с ошибкой."""
    detail: str
    status_code: int
    error_code: Optional[str] = None
    extra: Optional[dict] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Ответ с пагинацией."""
    items: List[T]
    total: int
    page: int = Field(..., ge=1)
    per_page: int = Field(..., ge=1, le=100)
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1
