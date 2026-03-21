from fastapi import APIRouter, Query

from app.schemas import HealthResponse, MlProxyResponse
from app.services.ml import calculate_ml_score

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health():
    return {
        "status": "ok"
    }


@router.get("/score", response_model=MlProxyResponse)
async def score(x: float = Query(..., description="Input value")):
    return await calculate_ml_score(x)