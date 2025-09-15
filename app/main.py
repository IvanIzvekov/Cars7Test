from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import employee_routers, coefficient_routers, shift_routers, break_shift_routers, statistics_routers
from app.core.database import init_models, shutdown_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_models()
        yield
    finally:
        await shutdown_engine()


app = FastAPI(title="Support Operators API", lifespan=lifespan)

app.include_router(employee_routers.router, prefix="/api/v1")
app.include_router(coefficient_routers.router, prefix="/api/v1")
app.include_router(shift_routers.router, prefix="/api/v1")
app.include_router(break_shift_routers.router, prefix="/api/v1")
app.include_router(statistics_routers.router, prefix="/api/v1")






