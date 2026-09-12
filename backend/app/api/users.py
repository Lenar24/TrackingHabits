"""
Модуль предоставляет эндпоинты для управления пользователями.
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserResponse, UserUpdate, UserWithHabits, MessageResponse
from ..services import UserService, HabitService
from ..utils.database import get_db
from ..utils.auth import get_current_user, get_current_admin

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Получение списка всех зарегистрированных пользователей.
    🔒 Только для администраторов.
    """
    return UserService.get_all_users(db, skip, limit)


@router.get("/me", response_model=UserWithHabits)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получение информации о текущем авторизованном пользователе.
    """
    habits = HabitService.get_habits(db, current_user.id, active_only=False)

    return UserWithHabits(
        id=current_user.id,
        max_user_id=current_user.max_user_id,
        username=current_user.username,
        chat_id=current_user.chat_id,
        is_admin=current_user.is_admin,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        habits=habits
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Получение информации о конкретном пользователе.
    Разрешено только для самого пользователя или админа.
    """
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление данных пользователя.
    Разрешено только для самого пользователя или админа.
    """
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    user = UserService.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/me/chat-id", response_model=UserResponse)
def update_my_chat_id(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Обновление chat_id текущего пользователя.
    """
    user = UserService.update_chat_id(db, current_user.max_user_id, chat_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Удаление пользователя.
    🔒 Только для администраторов.
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    logger.info(f"User {user_id} deleted by admin {current_user.id}")
    return MessageResponse(message="User deleted successfully")
