import httpx

from ..core.config import settings


class APIClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, verify=False)
        self.base_url = settings.API_URL

    async def get(self, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        print(f"🔍 URL: {url}")  # <-- Временное логирование

        return await self.client.get(f"{self.base_url}{endpoint}", **kwargs)

    async def post(self, endpoint: str, **kwargs):
        return await self.client.post(f"{self.base_url}{endpoint}", **kwargs)

    async def put(self, endpoint: str, **kwargs):
        return await self.client.put(f"{self.base_url}{endpoint}", **kwargs)

    async def delete(self, endpoint: str, **kwargs):
        return await self.client.delete(f"{self.base_url}{endpoint}", **kwargs)

    async def close(self):
        await self.client.aclose()
