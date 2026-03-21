import aiohttp

from app.clients.base import BaseServiceClient


class DataServiceClient(BaseServiceClient):
    def __init__(self, session: aiohttp.ClientSession, base_url: str) -> None:
        super().__init__(session=session, base_url=base_url)

    async def get_items(self) -> dict:
        return await self._get("/items")

    async def create_item(self, text: str) -> dict:
        return await self._post("/items", json={"text": text})