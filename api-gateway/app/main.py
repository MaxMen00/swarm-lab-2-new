from contextlib import asynccontextmanager

import aiohttp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.clients.data_service import DataServiceClient
from app.clients.load_service import LoadServiceClient
from app.clients.ml_service import MlServiceClient
from app.config import (
    DATA_SERVICE_URL,
    HTTP_TIMEOUT_SECONDS,
    LOAD_SERVICE_URL,
    ML_SERVICE_URL,
    SERVICE_NAME,
)
from app.routers.items import router as items_router
from app.routers.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT_SECONDS)
    session = aiohttp.ClientSession(timeout=timeout)

    app.state.http_session = session
    app.state.data_service_client = DataServiceClient(
        session=session,
        base_url=DATA_SERVICE_URL,
    )
    app.state.load_service_client = LoadServiceClient(
        session=session,
        base_url=LOAD_SERVICE_URL,
    )
    app.state.ml_service_client = MlServiceClient(
        session=session,
        base_url=ML_SERVICE_URL,
    )

    try:
        yield
    finally:
        await session.close()


app = FastAPI(
    title=SERVICE_NAME,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(items_router)