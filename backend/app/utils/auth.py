"""
Модуль для аутентификации и авторизации с JWT токенами.
"""

import logging
from typing import Optional
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models import User
from ..utils.database import get_db

logger = logging.getLogger(__name__)
security = HTTPBearer()


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Создание JWT токена доступа.

    Args:
        data: Данные для включения в токен
        expires_delta: Время жизни токена

    Returns:
        str: JWT токен
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Создание Refresh токена.

    Args:
        data: Данные для включения в токен

    Returns:
        str: Refresh токен
    """
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
) -> User:
    """
    Получение текущего пользователя из JWT токена.
    Поддерживает системные токены для внутренних вызовов.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )

        token_type = payload.get("type")
        if token_type == "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token not allowed for this endpoint",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id_str = payload.get("sub")
        if not user_id_str:
            logger.warning("Token missing 'sub' claim")
            raise credentials_exception

        # ✅ Поддержка системного токена
        if user_id_str == "system":
            logger.info("🔧 Системный токен — доступ разрешён")
            system_user = db.query(User).filter(User.is_admin == True).first()
            if not system_user:
                logger.error("❌ Нет админа для системного токена")
                raise credentials_exception
            return system_user

        try:
            user_id = int(user_id_str)
        except ValueError:
            logger.warning(f"Invalid user_id format: {user_id_str}")
            raise credentials_exception

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            logger.warning(f"Inactive user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        logger.debug(f"Authenticated user: {user_id}")
        return user

    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        logger.warning(f"JWT validation error: {e}")
        raise credentials_exception


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Проверяет, что текущий пользователь является администратором.

    Args:
        current_user: Текущий пользователь

    Returns:
        User: Пользователь с правами администратора

    Raises:
        HTTPException: 403 если пользователь не администратор
    """
    if not current_user.is_admin:
        logger.warning(f"Admin access denied for user {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    logger.debug(f"Admin access granted for user {current_user.id}")
    return current_user


def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Получение пользователя из токена (опционально).

    Используется для эндпоинтов, где авторизация не обязательна.
    """
    if not credentials:
        return None

    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None
