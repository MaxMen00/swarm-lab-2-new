from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import SERVICE_NAME
from app.redis_client import create_redis_client
from contextlib import asynccontextmanager
from app.routers.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = create_redis_client()

    app.state.redis_client = redis_client

    try:
        await redis_client.ping()
        yield
    finally:
        await redis_client.aclose()


app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)