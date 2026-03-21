from fastapi import APIRouter, Request

from app.config import HOSTNAME
from app.schemas import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health(request: Request):
    db_ready = bool(getattr(request.app.state, "db_ready", False))
    return {
        "status": "ok",
        "hostname": HOSTNAME,
        "db_status": "ready" if db_ready else "not-ready",
    }