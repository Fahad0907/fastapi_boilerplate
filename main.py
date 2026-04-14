from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_engine, Base
from auth.urls import router as auth_router
from middlewares import logging_middleware
from middlewares import error_middleware
from middlewares import http_exception_handler
from middlewares import validation_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="FastAPI Practice",
    description="Structured FastAPI application",
    version="1.0.0",
    lifespan=lifespan
)


# Register routers
app.include_router(auth_router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}


# middlewares
@app.middleware("http")
async def add_logging(request, call_next):
    return await logging_middleware(request, call_next)

@app.middleware("http")
async def add_error_handling(request, call_next):
    return await error_middleware(request, call_next)

# exception handlers
app.add_exception_handler(http_exception_handler)
app.add_exception_handler(validation_exception_handler)