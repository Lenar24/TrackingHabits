"""
Модуль предоставляет асинхронный HTTP клиент для взаимодействия с бэкенд API.
"""

from typing import Optional, Dict
import httpx

from ..core.config import settings


class APIClient:
    """
    Асинхронный HTTP клиент с поддержкой JWT-токенов.
    """

    def __init__(self):
        # ✅ Безопасная конфигурация
        verify_ssl = settings.ENVIRONMENT != "development"

        self.client = httpx.AsyncClient(
            timeout=30.0,
            verify=verify_ssl,
            follow_redirects=True,
        )
        self.base_url = settings.API_URL
        self._token: Optional[str] = None

    def set_token(self, token: str) -> None:
        """Установка JWT токена для последующих запросов."""
        self._token = token

    def clear_token(self) -> None:
        """Очистка токена."""
        self._token = None

    def _get_headers(self, headers: Optional[Dict] = None) -> Dict:
        """Формирование заголовков с автоматической подстановкой токена."""
        result = headers or {}
        result.setdefault("Content-Type", "application/json")

        if self._token:
            result["Authorization"] = f"Bearer {self._token}"

        return result

    async def request(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> httpx.Response:
        """Универсальный метод для выполнения HTTP запросов."""
        url = f"{self.base_url}{endpoint}"
        request_headers = self._get_headers(headers)

        return await self.client.request(
            method,
            url,
            headers=request_headers,
            **kwargs
        )

    async def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнение GET запроса."""
        return await self.request("GET", endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнение POST запроса."""
        return await self.request("POST", endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнение PUT запроса."""
        return await self.request("PUT", endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Выполнение DELETE запроса."""
        return await self.request("DELETE", endpoint, **kwargs)

    async def close(self) -> None:
        """Закрытие HTTP клиента."""
        await self.client.aclose()
