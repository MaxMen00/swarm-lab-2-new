import asyncio
import math
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from app.config import HOSTNAME


def thread_worker(seconds: int) -> int:
    end_time = time.monotonic() + seconds
    iterations = 0

    while time.monotonic() < end_time:
        iterations += 1
        math.sqrt((iterations % 1000) + 1)

    return iterations


async def run_thread_job(threads: int, seconds: int) -> dict:
    start_threads = threading.active_count()

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [loop.run_in_executor(executor, thread_worker, seconds) for _ in range(threads)]
        #futures = [executor.submit(thread_worker, seconds) for _ in range(threads)] блокирует event loop, т.к f.result() - синхронный вызов
        results = await asyncio.gather(*futures)
    end_threads = threading.active_count()

    return {
        "status": "completed",
        "backend_hostname": HOSTNAME,
        "threads_requested": threads,
        "seconds": seconds,
        "iterations": sum(results),
        "threads_before": start_threads,
        "threads_after": end_threads,
        "resource_hint": (
            "Для демонстрации scheduler/thread pressure попробуйте 50-300 потоков "
            "и наблюдайте docker stats / top / htop"
        ),
    }