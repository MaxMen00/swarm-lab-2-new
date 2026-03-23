from fastapi import APIRouter, Query, Request

from app.schemas import HealthResponse, MlProxyResponse
from app.services.ml import calculate_ml_score

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok"
    }


@router.get("/score", response_model=MlProxyResponse)
async def score(request: Request, x: float = Query(..., description="Input value")):
    redis_client = request.app.state.redis_client
    return await calculate_ml_score(x=x, redis_client=redis_client)