import aiohttp

from app.clients.base import BaseServiceClient


class MlServiceClient(BaseServiceClient):
    def __init__(self, session: aiohttp.ClientSession, base_url: str) -> None:
        super().__init__(session=session, base_url=base_url)

    async def score(self, x: float) -> dict:
        return await self._get("/score", params={"x": x})