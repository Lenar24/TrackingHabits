"""
Модуль предоставляет эндпоинты для получения расширенной статистики по привычкам
пользователя. Включает данные о прогрессе, сериях выполнения (стриках),
ежедневной активности и общей эффективности.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models import HabitLog
from ..services import HabitService
from ..utils.database import get_db

router = APIRouter(prefix="/habits", tags=["stats"])


@router.get("/{user_id}/stats")
def get_habit_stats(user_id: int, db: Session = Depends(get_db)):
    """Получение подробной статистики по всем привычкам пользователя (включая завершенные)."""
    habits = HabitService.get_habits(db, user_id, active_only=False)

    result = []
    for habit in habits:
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.id).order_by(HabitLog.date.desc()).limit(30).all()

        total_days = len(logs)
        completed_days = sum(1 for log in logs if log.completed)

        last_7_days = []
        for log in logs[:7]:
            last_7_days.append({"date": log.date.strftime("%d.%m"), "completed": log.completed})

        best_streak = 0
        current_streak = 0
        for log in sorted(logs, key=lambda x: x.date):
            if log.completed:
                current_streak += 1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 0

        result.append(
            {
                "id": habit.id,
                "name": habit.name,
                "is_active": habit.is_active,
                "days_completed": habit.days_completed,
                "max_days": habit.max_days,
                "completed_at": habit.completed_at,
                "created_at": habit.created_at,
                "total_logs": total_days,
                "completed_logs": completed_days,
                "best_streak": best_streak,
                "last_7_days": last_7_days,
            }
        )

    return result
