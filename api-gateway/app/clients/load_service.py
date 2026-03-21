import aiohttp

from app.clients.base import BaseServiceClient


class LoadServiceClient(BaseServiceClient):
    def __init__(self, session: aiohttp.ClientSession, base_url: str) -> None:
        super().__init__(session=session, base_url=base_url)

    async def heavy(self, seconds: int) -> dict:
        return await self._get("/heavy", params={"seconds": seconds})

    async def memory(self, megabytes: int, hold_seconds: int) -> dict:
        return await self._get(
            "/memory",
            params={"megabytes": megabytes, "hold_seconds": hold_seconds},
        )

    async def threads(self, threads: int, seconds: int) -> dict:
        return await self._get(
            "/threads",
            params={"threads": threads, "seconds": seconds},
        )