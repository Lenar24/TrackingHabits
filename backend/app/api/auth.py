"""
Модуль предоставляет эндпоинты для аутентификации пользователей.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.config import settings
from ..schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest
from ..schemas.common import MessageResponse
from ..services import UserService
from ..utils.database import get_db
from ..utils.auth import create_access_token, create_refresh_token, get_current_user
from ..models import User

logger = logging.getLogger(__name__)

# ✅ РОУТЕР СОЗДАН
router = APIRouter()


# ✅ РОУТ 1: Логин
@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Логин пользователя и выдача JWT токена.
    Если пользователь не существует — создаётся автоматически.
    """
    try:
        user = UserService.get_or_create_user(
            db,
            max_user_id=request.user_id,
            username=request.username,
            chat_id=request.chat_id
        )

        token_data = {
            "sub": str(user.id),
            "user_id": user.id,
            "max_user_id": user.max_user_id,
            "chat_id": user.chat_id,
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        logger.info(f"User {user.id} logged in successfully")

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_token=refresh_token
        )

    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to login"
        )


# ✅ РОУТ 2: Обновление токена
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Обновление access токена с использованием refresh токена.
    """
    try:
        from jose import jwt, JWTError

        payload = jwt.decode(
            request.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )

        user_id = int(payload.get("sub"))
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        token_data = {
            "sub": str(user.id),
            "user_id": user.id,
            "max_user_id": user.max_user_id,
            "chat_id": user.chat_id,
        }

        new_access_token = create_access_token(token_data)

        return TokenResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


# ✅ РОУТ 3: Получение информации о текущем пользователе
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Получение информации о текущем пользователе.
    """
    return {
        "id": current_user.id,
        "max_user_id": current_user.max_user_id,
        "username": current_user.username,
        "chat_id": current_user.chat_id,
        "is_admin": current_user.is_admin,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at,
    }


# ✅ РОУТ 4: Выход
@router.post("/logout", response_model=MessageResponse)
def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Выход пользователя (клиентская сторона должна удалить токен).
    """
    logger.info(f"User {current_user.id} logged out")
    return MessageResponse(message="Successfully logged out")
