"""
Класс UserService реализует бизнес-логику работы с пользователями.
"""

from typing import Optional, List, Dict, Any
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from ..models import User, Habit
from ..schemas import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserService:
    """Сервис для работы с пользователями."""

    # ============ ПОЛУЧЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ============

    @staticmethod
    def get_user_by_max_id(db: Session, max_user_id: int) -> Optional[User]:
        """
        Получение пользователя по MAX user_id.

        Args:
            db: Сессия базы данных
            max_user_id: ID пользователя из MAX

        Returns:
            Optional[User]: Найденный пользователь или None
        """
        try:
            return db.query(User).filter(User.max_user_id == max_user_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении пользователя по max_user_id {max_user_id}: {e}")
            raise

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Получение пользователя по внутреннему ID.

        Args:
            db: Сессия базы данных
            user_id: Внутренний ID пользователя

        Returns:
            Optional[User]: Найденный пользователь или None
        """
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении пользователя по id {user_id}: {e}")
            raise

    @staticmethod
    def get_user_by_chat_id(db: Session, chat_id: int) -> Optional[User]:
        """
        Получение пользователя по chat_id.

        Args:
            db: Сессия базы данных
            chat_id: ID чата

        Returns:
            Optional[User]: Найденный пользователь или None
        """
        try:
            return db.query(User).filter(User.chat_id == chat_id).first()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении пользователя по chat_id {chat_id}: {e}")
            raise

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Получение всех пользователей с пагинацией.

        Args:
            db: Сессия базы данных
            skip: Количество пропускаемых записей
            limit: Лимит записей

        Returns:
            List[User]: Список пользователей
        """
        try:
            return db.query(User).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении всех пользователей: {e}")
            raise

    @staticmethod
    def get_users_with_habits(
            db: Session,
            skip: int = 0,
            limit: int = 100
    ) -> List[User]:
        """
        Получение пользователей с загрузкой привычек.

        Args:
            db: Сессия базы данных
            skip: Количество пропускаемых записей
            limit: Лимит записей

        Returns:
            List[User]: Список пользователей с привычками
        """
        try:
            return db.query(User).options(
                joinedload(User.habits)
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении пользователей с привычками: {e}")
            raise

    @staticmethod
    def get_active_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Получение активных пользователей.

        Args:
            db: Сессия базы данных
            skip: Количество пропускаемых записей
            limit: Лимит записей

        Returns:
            List[User]: Список активных пользователей
        """
        try:
            return db.query(User).filter(
                User.is_active == True
            ).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка БД при получении активных пользователей: {e}")
            raise

    # ============ СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ ============

    @staticmethod
    def create_user(
            db: Session,
            max_user_id: int,
            chat_id: int,
            username: Optional[str] = None
    ) -> User:
        """
        Создание нового пользователя.

        Args:
            db: Сессия базы данных
            max_user_id: ID пользователя из MAX
            chat_id: ID чата
            username: Имя пользователя

        Returns:
            User: Созданный пользователь

        Raises:
            ValueError: Если пользователь уже существует или chat_id не указан
        """
        # Проверка существования
        existing = UserService.get_user_by_max_id(db, max_user_id)
        if existing:
            raise ValueError(f"Пользователь с max_user_id={max_user_id} уже существует")

        # Валидация
        if not chat_id:
            raise ValueError("chat_id обязателен")

        db_user = User(
            max_user_id=max_user_id,
            chat_id=chat_id,
            username=username.strip() if username else None
        )

        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"✅ Создан пользователь: max_user_id={max_user_id}, chat_id={chat_id}")
            return db_user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при создании пользователя {max_user_id}: {e}")
            raise

    # ============ ОБНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ============

    @staticmethod
    def update_chat_id(db: Session, max_user_id: int, chat_id: int) -> Optional[User]:
        """
        Обновление chat_id пользователя.

        Args:
            db: Сессия базы данных
            max_user_id: ID пользователя из MAX
            chat_id: Новый ID чата

        Returns:
            Optional[User]: Обновленный пользователь или None
        """
        user = UserService.get_user_by_max_id(db, max_user_id)
        if not user:
            logger.warning(f"⚠️ Пользователь {max_user_id} не найден для обновления chat_id")
            return None

        if user.chat_id == chat_id:
            return user

        try:
            user.chat_id = chat_id
            db.commit()
            db.refresh(user)
            logger.info(f"✅ Обновлен chat_id для пользователя {max_user_id}: {chat_id}")
            return user
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при обновлении chat_id для {max_user_id}: {e}")
            raise

    @staticmethod
    def update_user(db: Session, max_user_id: int, user_update: UserUpdate) -> Optional[User]:
        """
        Обновление данных пользователя.

        Args:
            db: Сессия базы данных
            max_user_id: ID пользователя из MAX
            user_update: Данные для обновления

        Returns:
            Optional[User]: Обновленный пользователь или None
        """
        user = UserService.get_user_by_max_id(db, max_user_id)
        if not user:
            return None

        try:
            if user_update.username is not None:
                user.username = user_update.username.strip() if user_update.username else None

            if user_update.chat_id is not None:
                user.chat_id = user_update.chat_id

            if user_update.is_admin is not None:
                user.is_admin = user_update.is_admin

            if user_update.is_active is not None:
                user.is_active = user_update.is_active

            db.commit()
            db.refresh(user)
            logger.info(f"✅ Обновлен пользователь {max_user_id}")
            return user

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при обновлении пользователя {max_user_id}: {e}")
            raise

    # ============ УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ============

    @staticmethod
    def delete_user(db: Session, user_id: int, admin_id: Optional[int] = None) -> bool:
        """
        Удаление пользователя.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя
            admin_id: ID администратора (для логирования)

        Returns:
            bool: True если удаление успешно

        Raises:
            ValueError: Если пользователь администратор
        """
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                return False

            # Нельзя удалить администратора
            if user.is_admin:
                raise ValueError("Нельзя удалить администратора")

            db.delete(user)
            db.commit()

            logger.info(f"✅ Удален пользователь {user_id} администратором {admin_id}")
            return True

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"❌ Ошибка БД при удалении пользователя {user_id}: {e}")
            raise

    # ============ GET OR CREATE ============

    @staticmethod
    def get_or_create_user(
            db: Session,
            max_user_id: int,
            chat_id: int,
            username: Optional[str] = None
    ) -> User:
        """
        Получение или создание пользователя.

        Args:
            db: Сессия базы данных
            max_user_id: ID пользователя из MAX
            chat_id: ID чата
            username: Имя пользователя

        Returns:
            User: Существующий или созданный пользователь
        """
        user = UserService.get_user_by_max_id(db, max_user_id)

        if user:
            # Обновляем chat_id если изменился
            if chat_id and user.chat_id != chat_id:
                user = UserService.update_chat_id(db, max_user_id, chat_id)
            return user

        # Создаем нового пользователя
        return UserService.create_user(db, max_user_id, chat_id, username)

    # ============ СТАТИСТИКА ============

    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Получение статистики пользователя.

        Args:
            db: Сессия базы данных
            user_id: ID пользователя

        Returns:
            Dict: Статистика пользователя

        Raises:
            ValueError: Если пользователь не найден
        """
        try:
            user = UserService.get_user_by_id(db, user_id)
            if not user:
                raise ValueError("Пользователь не найден")

            total_habits = user.habits.count()
            active_habits = user.habits.filter(Habit.is_active == True).count()
            completed_habits = total_habits - active_habits

            # Общее количество выполненных дней
            total_days = db.query(db.func.sum(Habit.days_completed)).filter(
                Habit.user_id == user_id
            ).scalar() or 0

            return {
                "user_id": user.id,
                "max_user_id": user.max_user_id,
                "username": user.username,
                "chat_id": user.chat_id,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
                "total_habits": total_habits,
                "active_habits": active_habits,
                "completed_habits": completed_habits,
                "total_days_completed": total_days,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при получении статистики пользователя {user_id}: {e}")
            raise

    # ============ ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ============

    @staticmethod
    def count_users(db: Session) -> int:
        """
        Подсчет общего количества пользователей.

        Args:
            db: Сессия базы данных

        Returns:
            int: Количество пользователей
        """
        try:
            return db.query(User).count()
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при подсчете пользователей: {e}")
            raise

    @staticmethod
    def count_active_users(db: Session) -> int:
        """
        Подсчет количества активных пользователей.

        Args:
            db: Сессия базы данных

        Returns:
            int: Количество активных пользователей
        """
        try:
            return db.query(User).filter(User.is_active == True).count()
        except SQLAlchemyError as e:
            logger.error(f"❌ Ошибка БД при подсчете активных пользователей: {e}")
            raise
