"""
Класс UserService реализует бизнес-логику работы с пользователями.
Содержит методы для получения, создания и обновления пользователей в системе.
Используется для управления пользователями, их идентификаторами и контактными данными.
"""

from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate


class UserService:
    """Класс UserService"""

    @staticmethod
    def get_user(db: Session, user_id: int):
        """Получение пользователя по его уникальному ID в MAX."""
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """Создание нового пользователя в системе."""
        db_user = User(user_id=user.user_id, chat_id=user.chat_id, username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_chat_id(db: Session, user_id: int, chat_id: int):
        """Обновление идентификатора чата для пользователя."""
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.chat_id = chat_id
            db.commit()
            db.refresh(user)
        return user
