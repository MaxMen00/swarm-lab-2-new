from pydantic import BaseModel
from app.config import HOSTNAME

class HealthResponse(BaseModel):
    status: str
    hostname: str = HOSTNAME


class MlProxyResponse(BaseModel):
    backend_hostname: str = HOSTNAME
    score: float
    gpu_node: bool
    explanation: str
    cache_hit: bool
    cache_key: str


