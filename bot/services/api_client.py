"""
Модуль предоставляет асинхронный HTTP клиент для взаимодействия с внутренним бэкенд API.
Оборачивает библиотеку httpx и предоставляет удобные методы для выполнения HTTP запросов
с автоматической подстановкой базового URL и общих настроек.
"""

import httpx

from ..core.config import settings


class APIClient:
    """Инициализация HTTP клиента с настройками."""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, verify=False)
        self.base_url = settings.API_URL

    async def get(self, endpoint: str, **kwargs):
        """Выполнение GET запроса к бэкенд API."""
        return await self.client.get(f"{self.base_url}{endpoint}", **kwargs)

    async def post(self, endpoint: str, **kwargs):
        """Выполнение POST запроса к бэкенд API."""
        return await self.client.post(f"{self.base_url}{endpoint}", **kwargs)

    async def put(self, endpoint: str, **kwargs):
        """Выполнение PUT запроса к бэкенд API."""
        return await self.client.put(f"{self.base_url}{endpoint}", **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        """Выполнение DELETE запроса к бэкенд API."""
        return await self.client.delete(f"{self.base_url}{endpoint}", **kwargs)

    async def close(self):
        """Закрытие HTTP клиента и освобождение ресурсов."""
        await self.client.aclose()
