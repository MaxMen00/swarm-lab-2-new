from fastapi import APIRouter, Depends

from app.clients.data_service import DataServiceClient
from app.config import HOSTNAME
from app.deps import get_data_service_client
from app.schemas import CreateItemResponse, ItemIn, ItemsListResponse

router = APIRouter(tags=["items"])


@router.get("/api/items", response_model=ItemsListResponse)
async def get_items(
    data_client: DataServiceClient = Depends(get_data_service_client),
):
    response = await data_client.get_items()
    return {
        "backend_hostname": response["backend_hostname"],
        "items": response["items"],
    }


@router.post("/api/items", response_model=CreateItemResponse)
async def create_item(
    item: ItemIn,
    data_client: DataServiceClient = Depends(get_data_service_client),
):
    response = await data_client.create_item(item.text)
    return {
        "backend_hostname": response["backend_hostname"],
        "item": response["item"],
    }