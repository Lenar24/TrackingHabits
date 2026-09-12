"""
Модуль предоставляет эндпоинты для управления напоминаниями.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import MessageResponse
from ..scheduler import send_test_reminder, run_reminder_now
from ..utils.database import get_db
from ..utils.auth import get_current_user, get_current_admin
from ..models import User

router = APIRouter()


@router.post("/test", response_model=MessageResponse)
async def test_reminder(
    user_id: int,
    chat_id: int,
    current_user: User = Depends(get_current_admin)
):
    """
    Тестовый эндпоинт для проверки отправки напоминаний.
    🔒 Только для администраторов.
    """
    try:
        success = await send_test_reminder(user_id, chat_id)
        if success:
            return MessageResponse(
                message=f"Test reminder sent to user {user_id}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to send test reminder"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/run-now", response_model=MessageResponse)
async def run_reminders_now(
    current_user: User = Depends(get_current_admin)
):
    """
    Принудительный запуск рассылки напоминаний.
    🔒 Только для администраторов.
    """
    try:
        result = await run_reminder_now()
        return MessageResponse(
            message=f"Reminders sent: {result.get('successful', 0)} successful, {result.get('failed', 0)} failed",
            data=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
