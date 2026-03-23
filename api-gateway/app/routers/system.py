from fastapi import APIRouter, Depends, Query

from app.clients.data_service import DataServiceClient
from app.clients.load_service import LoadServiceClient
from app.clients.ml_service import MlServiceClient
from app.config import HOSTNAME
from app.deps import (
    get_data_service_client,
    get_load_service_client,
    get_ml_service_client,
)
from app.schemas import (
    HealthResponse,
    HeavyResponse,
    InfoResponse,
    ServicesInfoResponse,
    MemoryResponse,
    MlProxyResponse,
    ThreadsResponse,
)
from app.services.info import build_info, build_info_services

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok",
        "hostname": HOSTNAME,
    }

@router.get("/api/info", response_model=InfoResponse)
async def info():
    return await build_info()

@router.get("/api/info/services", response_model=ServicesInfoResponse)
async def info_services(
    data_client: DataServiceClient = Depends(get_data_service_client),
    load_client: LoadServiceClient = Depends(get_load_service_client),
    ml_client: MlServiceClient = Depends(get_ml_service_client),
):
    return await build_info_services(data_client, load_client, ml_client)

@router.get("/api/ml-proxy", response_model=MlProxyResponse)
async def ml_proxy(
    x: float = Query(..., description="Input value"),
    ml_client: MlServiceClient = Depends(get_ml_service_client),
):
    response = await ml_client.score(x)
    return {
        "backend_hostname": response["backend_hostname"],
        "score": response["score"],
        "gpu_node": response["gpu_node"],
        "explanation": response["explanation"],
        "cache_hit": response["cache_hit"],
        "cache_key": response["cache_key"],
    }


@router.get("/api/heavy", response_model=HeavyResponse)
async def heavy(
    seconds: int = Query(5, ge=1, le=30),
    load_client: LoadServiceClient = Depends(get_load_service_client),
):
    response = await load_client.heavy(seconds)
    return {
        "status": response["status"],
        "backend_hostname": response["backend_hostname"],
        "seconds": response["seconds"],
        "iterations": response["iterations"],
        "resource_hint": response["resource_hint"],
    }


@router.get("/api/memory", response_model=MemoryResponse)
async def memory(
    megabytes: int = Query(256, ge=1, le=2048),
    hold_seconds: int = Query(10, ge=1, le=300),
    load_client: LoadServiceClient = Depends(get_load_service_client),
):
    response = await load_client.memory(megabytes, hold_seconds)
    return {
        "status": response["status"],
        "backend_hostname": response["backend_hostname"],
        "requested_mb": response["requested_mb"],
        "allocated_mb": response["allocated_mb"],
        "hold_seconds": response["hold_seconds"],
        "resource_hint": response["resource_hint"],
    }


@router.get("/api/threads", response_model=ThreadsResponse)
async def threads(
    threads: int = Query(50, ge=1, le=500),
    seconds: int = Query(10, ge=1, le=60),
    load_client: LoadServiceClient = Depends(get_load_service_client),
):
    response = await load_client.threads(threads, seconds)
    return {
        "status": response["status"],
        "backend_hostname": response["backend_hostname"],
        "threads_requested": response["threads_requested"],
        "seconds": response["seconds"],
        "iterations": response["iterations"],
        "threads_before": response["threads_before"],
        "threads_after": response["threads_after"],
        "resource_hint": response["resource_hint"],
    }