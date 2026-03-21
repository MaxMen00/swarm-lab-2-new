from collections.abc import AsyncIterator

import asyncpg
from fastapi import Request

from app.db import acquire_connection


async def get_db_conn(request: Request) -> AsyncIterator[asyncpg.Connection]:
    async for connection in acquire_connection(request.app):
        yield connection