"""
Тесты для пользователей.
"""

import pytest


class TestUsers:
    """Тесты пользователей."""

    def test_get_me(self, client, auth_headers, test_user):
        """Получение информации о себе."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id

    def test_update_chat_id(self, client, auth_headers, test_user):
        """Обновление chat_id."""
        new_chat_id = 111222
        response = client.put(
            "/api/v1/users/me/chat-id",
            headers=auth_headers,
            params={"chat_id": new_chat_id}
        )
        assert response.status_code == 200

    def test_get_all_users_admin(self, client, admin_headers):
        """Получение всех пользователей (админ)."""
        response = client.get("/api/v1/users/", headers=admin_headers)
        assert response.status_code == 200

    def test_get_all_users_not_admin(self, client, auth_headers):
        """Получение всех пользователей (не админ)."""
        response = client.get("/api/v1/users/", headers=auth_headers)
        assert response.status_code == 403
