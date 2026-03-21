from fastapi import Request

from app.clients.data_service import DataServiceClient
from app.clients.load_service import LoadServiceClient
from app.clients.ml_service import MlServiceClient


def get_data_service_client(request: Request) -> DataServiceClient:
    return request.app.state.data_service_client


def get_load_service_client(request: Request) -> LoadServiceClient:
    return request.app.state.load_service_client


def get_ml_service_client(request: Request) -> MlServiceClient:
    return request.app.state.ml_service_client