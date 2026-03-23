from pydantic import BaseModel, Field


class ItemIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)


class ItemOut(BaseModel):
    id: int
    text: str
    created_at: str


class ItemsListResponse(BaseModel):
    backend_hostname: str
    items: list[ItemOut]


class CreateItemResponse(BaseModel):
    backend_hostname: str
    item: ItemOut


class HealthResponse(BaseModel):
    status: str
    hostname: str


class InfoResponse(BaseModel):
    service: str
    hostname: str
    timestamp: str


class ServiceInfoResponse(BaseModel):
    status: str
    hostname: str


class DataServiceInfoResponse(BaseModel):
    status: str
    hostname: str
    db_status: str


class ServicesInfoResponse(BaseModel):
    service: str
    hostname: str
    timestamp: str
    upstreams: dict[str, dict]


class MlProxyResponse(BaseModel):
    backend_hostname: str
    score: float
    gpu_node: bool
    explanation: str
    cache_hit: bool
    cache_key: str


class HeavyResponse(BaseModel):
    status: str
    backend_hostname: str
    seconds: int
    iterations: int
    resource_hint: str


class MemoryResponse(BaseModel):
    status: str
    backend_hostname: str
    requested_mb: int
    allocated_mb: int
    hold_seconds: int
    resource_hint: str


class ThreadsResponse(BaseModel):
    status: str
    backend_hostname: str
    threads_requested: int
    seconds: int
    iterations: int
    threads_before: int
    threads_after: int
    resource_hint: str