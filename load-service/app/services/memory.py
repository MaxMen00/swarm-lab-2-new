import asyncio

from app.config import HOSTNAME


async def run_memory_job(megabytes: int, hold_seconds: int, chunk_mb: int = 10) -> dict:
    chunks: list[bytearray] = []
    allocated_mb = 0

    chunk_size = chunk_mb * 1024 * 1024

    while allocated_mb < megabytes:
        chunks.append(bytearray(chunk_size))
        allocated_mb += chunk_mb
        await asyncio.sleep(0)

    await asyncio.sleep(hold_seconds)

    return {
        "status": "completed",
        "backend_hostname": HOSTNAME,
        "requested_mb": megabytes,
        "allocated_mb": allocated_mb,
        "hold_seconds": hold_seconds,
        "resource_hint": (
            "Для демонстрации memory limits попробуйте 256-2048 mb "
            "и наблюдайте docker stats / top / htop"
        ),
    }