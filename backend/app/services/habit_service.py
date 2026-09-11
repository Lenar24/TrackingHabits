"""
Класс HabitService реализует бизнес-логику работы с привычками.
Содержит методы для создания, получения, обновления привычек,
а также для отметки выполнения, пропуска и завершения.
Реализует систему отслеживания привычек по методу "21 день".
"""

from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models import Habit, HabitLog, User
from ..schemas import HabitCreate, HabitUpdate

logger = logging.getLogger(__name__)


class HabitService:
    """
    Сервис для работы с привычками.
    Использует бизнес-логику, инкапсулированную в модели Habit.
    """

    # ============ CRUD ОПЕРАЦИИ ============

    @staticmethod
    def create_habit(db: Session, user_id: int, habit_data: HabitCreate) -> Habit:
        """
        Создание новой привычки.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя
            habit_data: Данные для создания привычки

        Returns:
            Habit: Созданная привычка

        Raises:
            ValueError: Если данные невалидны или привычка уже существует
        """
        # Валидация названия
        if not habit_data.name or not habit_data.name.strip():
            raise ValueError("Название привычки не может быть пустым")

        if len(habit_data.name) > Habit.MAX_NAME_LENGTH:
            raise ValueError(
                f"Название привычки не может превышать {Habit.MAX_NAME_LENGTH} символов"
            )

        # Проверка на дубликаты
        existing = db.query(Habit).filter(
            Habit.user_id == user_id,
            Habit.name == habit_data.name.strip(),
            Habit.is_active == True
        ).first()

        if existing:
            raise ValueError("Привычка с таким названием уже существует")

        # Создаем привычку (валидация внутри модели)
        try:
            db_habit = Habit(
                user_id=user_id,
                name=habit_data.name.strip(),
                description=habit_data.description.strip() if habit_data.description else None,
                max_days=habit_data.max_days or Habit.MAX_DAYS_DEFAULT
            )

            db.add(db_habit)
            db.commit()
            db.refresh(db_habit)

            logger.info(f"✅ Создана привычка id={db_habit.id} для пользователя {user_id}")
            return db_habit

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при создании привычки: {e}")
            raise

    @staticmethod
    def get_habits(
        db: Session,
        user_id: int,
        active_only: bool = True,
        skip: int = 0,
        limit: int = 100
    ) -> List[Habit]:
        """
        Получение списка привычек пользователя с пагинацией.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя
            active_only: Только активные привычки
            skip: Количество пропускаемых записей
            limit: Лимит записей

        Returns:
            List[Habit]: Список привычек
        """
        try:
            query = db.query(Habit).filter(Habit.user_id == user_id)

            if active_only:
                query = query.filter(Habit.is_active == True)

            return query.order_by(Habit.created_at.desc()).offset(skip).limit(limit).all()

        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении привычек: {e}")
            raise

    @staticmethod
    def get_habit(db: Session, habit_id: int) -> Optional[Habit]:
        """
        Получение привычки по ID.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Optional[Habit]: Найденная привычка или None
        """
        try:
            return db.query(Habit).filter(Habit.id == habit_id).first()
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении привычки {habit_id}: {e}")
            raise

    @staticmethod
    def get_habit_with_user(db: Session, habit_id: int) -> Optional[tuple[Habit, User]]:
        """
        Получение привычки вместе с владельцем.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Optional[tuple[Habit, User]]: Кортеж (привычка, пользователь) или None
        """
        try:
            result = db.query(Habit, User).join(User, Habit.user_id == User.id).filter(
                Habit.id == habit_id
            ).first()
            return result
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении привычки {habit_id} с пользователем: {e}")
            raise

    @staticmethod
    def update_habit(
        db: Session,
        habit_id: int,
        habit_update: HabitUpdate
    ) -> Optional[Habit]:
        """
        Обновление привычки.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки
            habit_update: Данные для обновления

        Returns:
            Optional[Habit]: Обновленная привычка или None

        Raises:
            ValueError: Если данные невалидны
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            return None

        try:
            if habit_update.name is not None:
                if not habit_update.name.strip():
                    raise ValueError("Название привычки не может быть пустым")
                if len(habit_update.name) > Habit.MAX_NAME_LENGTH:
                    raise ValueError(
                        f"Название не может превышать {Habit.MAX_NAME_LENGTH} символов"
                    )
                habit.name = habit_update.name.strip()

            if habit_update.description is not None:
                if habit_update.description:
                    if len(habit_update.description) > Habit.MAX_DESCRIPTION_LENGTH:
                        raise ValueError(
                            f"Описание не может превышать {Habit.MAX_DESCRIPTION_LENGTH} символов"
                        )
                    habit.description = habit_update.description.strip()
                else:
                    habit.description = None

            if habit_update.is_active is not None:
                habit.is_active = habit_update.is_active
                if not habit.is_active and not habit.completed_at:
                    habit.completed_at = datetime.now()

            if habit_update.max_days is not None:
                if habit_update.max_days < Habit.MIN_DAYS:
                    raise ValueError(f"max_days должен быть не менее {Habit.MIN_DAYS}")
                if habit_update.max_days > Habit.MAX_DAYS_LIMIT:
                    raise ValueError(f"max_days не может превышать {Habit.MAX_DAYS_LIMIT}")
                habit.max_days = habit_update.max_days

            db.commit()
            db.refresh(habit)

            logger.info(f"✅ Обновлена привычка {habit_id}")
            return habit

        except ValueError as e:
            db.rollback()
            logger.warning(f"⚠️ Ошибка валидации при обновлении привычки {habit_id}: {e}")
            raise
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при обновлении привычки {habit_id}: {e}")
            raise

    @staticmethod
    def delete_habit(db: Session, habit_id: int) -> bool:
        """
        Удаление привычки.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            bool: True если удаление успешно
        """
        try:
            habit = HabitService.get_habit(db, habit_id)
            if not habit:
                return False

            db.delete(habit)
            db.commit()

            logger.info(f"✅ Удалена привычка {habit_id}")
            return True

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при удалении привычки {habit_id}: {e}")
            raise

    # ============ БИЗНЕС-ЛОГИКА ============

    @staticmethod
    def mark_completed(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Отметка выполнения привычки за сегодня.
        Использует метод complete_today() модели Habit.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Результат операции

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            # Используем бизнес-логику модели
            result = habit.complete_today()

            if result["success"]:
                db.commit()
                db.refresh(habit)
                logger.info(f"✅ Выполнена привычка {habit_id}: {result['progress']}")
            else:
                logger.warning(f"⚠️ Ошибка выполнения привычки {habit_id}: {result['message']}")

            return result

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при выполнении привычки {habit_id}: {e}")
            raise

    @staticmethod
    def mark_skipped(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Отметка пропуска выполнения привычки.
        Использует метод skip_today() модели Habit.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Результат операции

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            # Используем бизнес-логику модели
            result = habit.skip_today()

            if result["success"]:
                db.commit()
                db.refresh(habit)
                logger.info(f"✅ Пропущена привычка {habit_id}")
            else:
                logger.warning(f"⚠️ Ошибка пропуска привычки {habit_id}: {result['message']}")

            return result

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при пропуске привычки {habit_id}: {e}")
            raise

    @staticmethod
    def complete_early(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Досрочное завершение привычки.
        Использует метод complete_early() модели Habit.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Результат операции

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            # Используем бизнес-логику модели
            result = habit.complete_early()

            if result["success"]:
                db.commit()
                db.refresh(habit)
                logger.info(f"✅ Досрочно завершена привычка {habit_id}")
            else:
                logger.warning(f"⚠️ Ошибка досрочного завершения {habit_id}: {result['message']}")

            return result

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при досрочном завершении {habit_id}: {e}")
            raise

    @staticmethod
    def reset_habit(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Сброс прогресса привычки.
        Использует метод reset() модели Habit.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Результат операции

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            result = habit.reset()

            if result["success"]:
                db.commit()
                db.refresh(habit)
                logger.info(f"✅ Сброшен прогресс привычки {habit_id}")

            return result

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при сбросе привычки {habit_id}: {e}")
            raise

    @staticmethod
    def activate_habit(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Активация завершенной привычки.
        Использует метод activate() модели Habit.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Результат операции

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            result = habit.activate()

            if result["success"]:
                db.commit()
                db.refresh(habit)
                logger.info(f"✅ Активирована привычка {habit_id}")

            return result

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при активации привычки {habit_id}: {e}")
            raise

    # ============ СТАТИСТИКА ============

    @staticmethod
    def get_habit_stats(db: Session, habit_id: int) -> Dict[str, Any]:
        """
        Получение статистики по привычке.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки

        Returns:
            Dict: Статистика привычки

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            logs = habit.logs.all()

            total_logs = len(logs)
            completed_logs = sum(1 for log in logs if log.completed)

            # Расчет текущего стрика
            current_streak = habit.get_streak()

            # Расчет лучшего стрика
            best_streak = 0
            streak = 0

            sorted_logs = sorted(logs, key=lambda x: x.date)
            for log in sorted_logs:
                if log.completed:
                    streak += 1
                    best_streak = max(best_streak, streak)
                else:
                    streak = 0

            return {
                "habit_id": habit.id,
                "name": habit.name,
                "total_logs": total_logs,
                "completed_logs": completed_logs,
                "skipped_logs": total_logs - completed_logs,
                "current_streak": current_streak,
                "best_streak": best_streak,
                "progress_percentage": habit.progress_percentage,
                "is_completed": habit.is_completed,
                "is_active": habit.is_active,
                "days_completed": habit.days_completed,
                "max_days": habit.max_days,
                "remaining_days": habit.remaining_days,
                "last_completed": habit.last_completed,
                "created_at": habit.created_at,
                "completed_at": habit.completed_at,
                "completed_early": habit.completed_early,
                "completion_rate": (completed_logs / total_logs * 100) if total_logs > 0 else 0
            }

        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении статистики привычки {habit_id}: {e}")
            raise

    @staticmethod
    def get_habit_history(
        db: Session,
        habit_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Получение истории выполнения привычки за последние N дней.

        Args:
            db: Сессия базы данных
            habit_id: ID привычки
            days: Количество дней

        Returns:
            Dict: История выполнения

        Raises:
            ValueError: Если привычка не найдена
        """
        habit = HabitService.get_habit(db, habit_id)
        if not habit:
            raise ValueError("Привычка не найдена")

        try:
            # Получаем логи за последние days дней
            start_date = date.today() - timedelta(days=days)

            logs = db.query(HabitLog).filter(
                HabitLog.habit_id == habit_id,
                HabitLog.date >= start_date
            ).order_by(HabitLog.date.desc()).all()

            # Создаем словарь для быстрого доступа
            log_dict = {log.date: log.completed for log in logs}

            # Заполняем все дни
            history = []
            for i in range(days - 1, -1, -1):
                current_date = date.today() - timedelta(days=i)
                history.append({
                    "date": current_date.isoformat(),
                    "day": current_date.strftime("%a"),  # Пн, Вт, Ср...
                    "completed": log_dict.get(current_date, False)
                })

            return {
                "habit_id": habit.id,
                "name": habit.name,
                "days": days,
                "history": history,
                "completed_count": sum(1 for h in history if h["completed"]),
                "completion_rate": (sum(1 for h in history if h["completed"]) / days * 100) if days > 0 else 0
            }

        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении истории привычки {habit_id}: {e}")
            raise

    @staticmethod
    def check_21_days(
        db: Session,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Проверка привычек на соответствие правилу 21 дня.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя (если None - проверяет всех)

        Returns:
            Dict: Статистика проверки
        """
        today = date.today()

        # Базовый запрос - активные привычки
        query = db.query(Habit).filter(Habit.is_active == True)

        if user_id is not None:
            query = query.filter(Habit.user_id == user_id)

        habits = query.all()

        updated_count = 0
        completed_count = 0
        errors = []

        for habit in habits:
            try:
                # Проверка пропуска дней
                if habit.last_completed:
                    days_since_last = (today - habit.last_completed).days
                    if days_since_last > 1:
                        # Сброс прогресса при длительном пропуске
                        habit.days_completed = 0
                        habit.last_completed = None
                        updated_count += 1
                        logger.warning(
                            f"⚠️ Сброшен прогресс привычки {habit.id} "
                            f"(не выполнялась {days_since_last} дней)"
                        )

                # Проверка достижения цели
                if habit.days_completed >= habit.max_days:
                    habit.is_active = False
                    habit.completed_at = datetime.now()
                    completed_count += 1
                    logger.info(f"✅ Привычка {habit.id} достигла цели автоматически")

            except Exception as e:
                errors.append(f"Ошибка при проверке привычки {habit.id}: {e}")
                logger.error(f"❌ Ошибка при проверке привычки {habit.id}: {e}")

        try:
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при сохранении изменений: {e}")
            raise

        return {
            "updated": updated_count,
            "completed": completed_count,
            "errors": errors,
            "total_checked": len(habits)
        }

    # ============ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ============

    @staticmethod
    def get_active_habits_count(db: Session, user_id: int) -> int:
        """
        Получение количества активных привычек пользователя.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя

        Returns:
            int: Количество активных привычек
        """
        try:
            return db.query(Habit).filter(
                Habit.user_id == user_id,
                Habit.is_active == True
            ).count()
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при подсчете активных привычек: {e}")
            raise

    @staticmethod
    def get_completed_habits_count(db: Session, user_id: int) -> int:
        """
        Получение количества завершенных привычек пользователя.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя

        Returns:
            int: Количество завершенных привычек
        """
        try:
            return db.query(Habit).filter(
                Habit.user_id == user_id,
                Habit.is_active == False
            ).count()
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при подсчете завершенных привычек: {e}")
            raise

    @staticmethod
    def get_total_days_completed(db: Session, user_id: int) -> int:
        """
        Получение общего количества выполненных дней по всем привычкам.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя

        Returns:
            int: Общее количество выполненных дней
        """
        try:
            result = db.query(db.func.sum(Habit.days_completed)).filter(
                Habit.user_id == user_id
            ).scalar()
            return result or 0
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при подсчете выполненных дней: {e}")
            raise
