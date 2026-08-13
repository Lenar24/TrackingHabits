"""
Модуль предоставляет эндпоинты для управления напоминаниями о привычках.
В текущей реализации содержит тестовый эндпоинт для ручной проверки системы отправки напоминаний.
"""

from fastapi import APIRouter

from ..scheduler import send_daily_reminders

router = APIRouter(prefix="/reminders", tags=["reminders"])


@router.post("/test")
async def test_reminders():
    """Тестовый эндпоинт для проверки отправки напоминаний"""
    await send_daily_reminders()
    return {"message": "Напоминания отправлены"}
