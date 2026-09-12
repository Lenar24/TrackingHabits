"""
Тесты для аутентификации.
"""

import pytest
from datetime import timedelta

from backend.app.utils.auth import create_access_token


class TestLogin:
    """Тесты логина."""

    def test_login_new_user(self, client, db_session):
        """Создание нового пользователя через логин."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "max_user_id": 11111,
                "chat_id": 22222,
                "username": "new_user",
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 1800

    def test_login_existing_user(self, client, test_user):
        """Логин существующего пользователя."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "max_user_id": test_user.max_user_id,
                "chat_id": test_user.chat_id,
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_updates_chat_id(self, client, test_user, db_session):
        """Обновление chat_id при логине."""
        new_chat_id = 999999
        response = client.post(
            "/api/v1/auth/login",
            json={
                "max_user_id": test_user.max_user_id,
                "chat_id": new_chat_id,
            }
        )
        assert response.status_code == 200

        db_session.refresh(test_user)
        assert test_user.chat_id == new_chat_id

    def test_login_missing_fields(self, client):
        """Логин без обязательных полей."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "test"}
        )
        assert response.status_code == 422


class TestCurrentUser:
    """Тесты получения текущего пользователя."""

    def test_get_me(self, client, auth_headers, test_user):
        """Получение информации о себе."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["max_user_id"] == test_user.max_user_id
        assert data["username"] == test_user.username

    def test_get_me_no_token(self, client):
        """Получение информации без токена."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403  # HTTPBearer возвращает 403

    def test_get_me_invalid_token(self, client):
        """Получение информации с невалидным токеном."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_get_me_expired_token(self, client, test_user):
        """Получение информации с истёкшим токеном."""
        expired_token = create_access_token(
            {"sub": str(test_user.id)},
            expires_delta=timedelta(seconds=-1)
        )
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401


class TestRefreshToken:
    """Тесты обновления токена."""

    def test_refresh_token(self, client, test_user):
        """Обновление access токена."""
        # Логин
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "max_user_id": test_user.max_user_id,
                "chat_id": test_user.chat_id,
            }
        )
        refresh_token = login_response.json()["refresh_token"]

        # Обновление
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_refresh_invalid_token(self, client):
        """Обновление с невалидным токеном."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        assert response.status_code == 401


class TestLogout:
    """Тесты выхода."""

    def test_logout(self, client, auth_headers):
        """Выход из системы."""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "Successfully logged out" in data["message"]
