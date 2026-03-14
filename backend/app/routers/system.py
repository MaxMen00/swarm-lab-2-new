from datetime import datetime, timezone

from fastapi import APIRouter, FastAPI, Query, Request

from app.config import HOSTNAME, SERVICE_NAME
from app.schemas import (
    HealthResponse,
    HeavyResponse,
    InfoResponse,
    MemoryResponse,
    MlProxyResponse,
    ThreadsResponse,
)
from app.services.heavy import run_heavy_job
from app.services.ml import calculate_ml_score
from app.services.memory import run_memory_job
from app.services.threads import run_thread_job

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok", "hostname": HOSTNAME}


@router.get("/api/info", response_model=InfoResponse)
async def info(request: Request):
    app: FastAPI = request.app
    return {
        "service": SERVICE_NAME,
        "hostname": HOSTNAME,
        "db_status": "ready" if getattr(app.state, "db_ready", False) else "not-ready",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/api/ml-proxy", response_model=MlProxyResponse)
async def ml_proxy(x: float = Query(..., description="Input value")):
    return await calculate_ml_score(x)


@router.get("/api/heavy", response_model=HeavyResponse)
async def heavy(seconds: int = Query(5, ge=1, le=30)):
    return await run_heavy_job(seconds)

@router.get("/api/memory", response_model=MemoryResponse)
async def memory(megabytes: int = Query(256, ge=1, le=2048), hold_seconds: int = Query(10, ge=1, le=300)):
    return await run_memory_job(megabytes, hold_seconds)

@router.get("/api/threads", response_model=ThreadsResponse)
async def threads(threads: int = Query(50, ge=1, le=500), seconds: int = Query(10, ge=1, le=60)):
    return await run_thread_job(threads, seconds)