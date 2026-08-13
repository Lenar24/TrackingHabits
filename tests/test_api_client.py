"""
Тесты HTTP клиента.
"""

from unittest.mock import AsyncMock, patch

import pytest

from bot.services.api_client import APIClient


class TestAPIClient:
    """Тесты API клиента"""

    def test_api_client_initialization(self):
        """Тест инициализации клиента"""

        client = APIClient()
        assert client is not None
        assert client.base_url == "http://backend:8000"

    @pytest.mark.asyncio
    async def test_api_client_get(self):
        """Тест GET запроса"""

        client = APIClient()
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(status_code=200)
            response = await client.get("/users/")
            assert response.status_code == 200
            mock_get.assert_called_once()

    @pytest.mark.asyncio
    async def test_api_client_post(self):
        """Тест POST запроса"""

        client = APIClient()
        with patch("httpx.AsyncClient.post") as mock_post:
            mock_post.return_value = AsyncMock(status_code=201)
            response = await client.post("/habits/", json={"name": "Test"})
            assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_api_client_close(self):
        """Тест закрытия клиента"""

        client = APIClient()
        with patch("httpx.AsyncClient.aclose") as mock_close:
            await client.close()
            mock_close.assert_called_once()
