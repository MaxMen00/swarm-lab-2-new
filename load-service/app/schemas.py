from pydantic import BaseModel
from app.config import HOSTNAME

class HealthResponse(BaseModel):
    status: str
    hostname: str = HOSTNAME


class HeavyResponse(BaseModel):
    status: str
    seconds: int
    iterations: int
    resource_hint: str
    backend_hostname: str = HOSTNAME


class MemoryResponse(BaseModel):
    status: str
    requested_mb: int
    allocated_mb: int
    hold_seconds: int
    resource_hint: str
    backend_hostname: str = HOSTNAME


class ThreadsResponse(BaseModel):
    status: str
    threads_requested: int
    seconds: int
    iterations: int
    threads_before: int
    threads_after: int
    resource_hint: str
    backend_hostname: str = HOSTNAME