from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        db_user = User(user_id=user.user_id, chat_id=user.chat_id, username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_chat_id(db: Session, user_id: int, chat_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.chat_id = chat_id
            db.commit()
            db.refresh(user)
        return user
