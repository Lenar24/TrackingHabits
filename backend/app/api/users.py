"""
Модуль предоставляет эндпоинты для управления пользователями системы.
Включает операции создания, получения, обновления пользователей,
а также специальную логику для работы с идентификаторами чатов в MAX.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import User as UserSchema
from ..schemas import UserCreate
from ..services import UserService
from ..utils.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserSchema])
def get_all_users(db: Session = Depends(get_db)):
    """Получение списка всех зарегистрированных пользователей."""
    return db.query(User).all()


@router.post("/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя или обновление chat_id для существующего."""
    existing_user = UserService.get_user(db, user.user_id)
    if existing_user:
        if existing_user.chat_id != user.chat_id:
            existing_user = UserService.update_chat_id(db, user.user_id, user.chat_id)
        return existing_user
    return UserService.create_user(db, user)


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Получение информации о конкретном пользователе."""
    db_user = UserService.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}/chat_id")
def update_chat_id(user_id: int, payload: dict, db: Session = Depends(get_db)):
    """Обновление ID чата для пользователя."""
    chat_id = payload.get("chat_id")
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    user = UserService.update_chat_id(db, user_id, chat_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
