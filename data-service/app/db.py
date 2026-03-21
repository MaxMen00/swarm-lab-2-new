import asyncio
from collections.abc import AsyncIterator

import asyncpg
from fastapi import FastAPI

from app.config import (
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    DB_COMMAND_TIMEOUT,
    DB_INIT_DELAY_SECONDS,
    DB_INIT_RETRIES,
    DB_POOL_MAX_SIZE,
    DB_POOL_MIN_SIZE,
)

CREATE_ITEMS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
)
"""


async def create_db_pool() -> asyncpg.Pool:
    return await asyncpg.create_pool(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD or None,
        database=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        min_size=DB_POOL_MIN_SIZE,
        max_size=DB_POOL_MAX_SIZE,
        command_timeout=DB_COMMAND_TIMEOUT,
    )


async def create_db_pool_with_retry() -> asyncpg.Pool:
    last_error: Exception | None = None

    for attempt in range(1, DB_INIT_RETRIES + 1):
        try:
            return await create_db_pool()
        except Exception as exc:
            last_error = exc
            if attempt == DB_INIT_RETRIES:
                break
            await asyncio.sleep(DB_INIT_DELAY_SECONDS)

    raise RuntimeError(
        f"Could not create DB pool after {DB_INIT_RETRIES} attempts: {last_error}"
    )


async def close_db_pool(pool: asyncpg.Pool | None) -> None:
    if pool is not None:
        await pool.close()


async def init_db(pool: asyncpg.Pool) -> bool:
    try:
        async with pool.acquire() as conn:
            await conn.execute(CREATE_ITEMS_TABLE_SQL)
        return True
    except Exception:
        return False


def get_db_pool(app: FastAPI) -> asyncpg.Pool:
    pool = getattr(app.state, "db_pool", None)
    if pool is None:
        raise RuntimeError("Database pool is not initialized")
    return pool


async def acquire_connection(app: FastAPI) -> AsyncIterator[asyncpg.Connection]:
    pool = get_db_pool(app)
    async with pool.acquire() as connection:
        yield connection