import aiohttp
from fastapi import HTTPException


class BaseServiceClient:
    def __init__(self, session: aiohttp.ClientSession, base_url: str) -> None:
        self.session = session
        self.base_url = base_url.rstrip("/")

    async def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        try:
            async with self.session.get(url, params=params) as response:
                if response.status >= 400:
                    text = await response.text()
                    raise HTTPException(
                        status_code=502,
                        detail=f"Upstream service returned HTTP {response.status}: {url}. Body: {text}",
                    )
                return await response.json()
        except aiohttp.ClientError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Upstream service is unavailable: {url}",
            ) from exc

    async def _post(self, path: str, json: dict | None = None) -> dict:
        url = f"{self.base_url}{path}"
        try:
            async with self.session.post(url, json=json) as response:
                if response.status >= 400:
                    text = await response.text()
                    raise HTTPException(
                        status_code=502,
                        detail=f"Upstream service returned HTTP {response.status}: {url}. Body: {text}",
                    )
                return await response.json()
        except aiohttp.ClientError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Upstream service is unavailable: {url}",
            ) from exc

    async def health(self) -> dict:
        return await self._get("/health")