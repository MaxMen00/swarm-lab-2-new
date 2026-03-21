from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    hostname: str
    db_status: str


class ItemIn(BaseModel):
    text: str = Field(..., min_length=1, max_length=10_000)


class ItemOut(BaseModel):
    id: int
    text: str
    created_at: datetime


class ItemsListResponse(BaseModel):
    backend_hostname: str
    items: list[ItemOut]


class CreateItemResponse(BaseModel):
    backend_hostname: str
    item: ItemOut