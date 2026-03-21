from fastapi import APIRouter, Query

from app.config import HOSTNAME
from app.schemas import (
    HealthResponse,
    HeavyResponse,
    MemoryResponse,
    ThreadsResponse,
)
from app.services.heavy import run_heavy_job
from app.services.memory import run_memory_job
from app.services.threads import run_thread_job

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
    }


@router.get("/heavy", response_model=HeavyResponse)
async def heavy(seconds: int = Query(5, ge=1, le=30)):
    return await run_heavy_job(seconds)


@router.get("/memory", response_model=MemoryResponse)
async def memory(
    megabytes: int = Query(256, ge=1, le=2048),
    hold_seconds: int = Query(10, ge=1, le=300),
):
    return await run_memory_job(megabytes, hold_seconds)


@router.get("/threads", response_model=ThreadsResponse)
async def threads(
    threads: int = Query(50, ge=1, le=500),
    seconds: int = Query(10, ge=1, le=60),
):
    return await run_thread_job(threads, seconds)