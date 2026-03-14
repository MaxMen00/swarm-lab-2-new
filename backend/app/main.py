from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import close_db_pool, create_db_pool, wait_for_db_and_init
from app.routers.items import router as items_router
from app.routers.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_db_pool()
    app.state.db_pool = pool
    app.state.db_ready = await wait_for_db_and_init(pool)

    try:
        yield
    finally:
        await close_db_pool(pool)


app = FastAPI(
    title="swarm-demo-backend",
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