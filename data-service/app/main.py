from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import SERVICE_NAME
from app.db import close_db_pool, create_db_pool_with_retry, init_db
from app.routers.items import router as items_router
from app.routers.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_db_pool_with_retry()
    app.state.db_pool = pool
    app.state.db_ready = await init_db(pool)

    try:
        yield
    finally:
        await close_db_pool(pool)


app = FastAPI(title=SERVICE_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(items_router)