import asyncio
import math

from app.config import HOSTNAME


async def run_heavy_job(seconds: int) -> dict:
    loop = asyncio.get_running_loop()
    start = loop.time()
    iterations = 0

    while loop.time() - start < seconds:
        for _ in range(10_000):
            iterations += 1
            math.sqrt((iterations % 1000) + 1)
        await asyncio.sleep(0)

    return {
        "status": "completed",
        "backend_hostname": HOSTNAME,
        "seconds": seconds,
        "iterations": iterations,
        "resource_hint": (
            "Для демонстрации limits/reservations попробуйте нагрузить процессор "
            "на 5-10 секунд и наблюдайте docker stats / top / htop"
        ),
    }