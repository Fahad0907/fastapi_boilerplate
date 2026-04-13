from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import get_engine, Base
from auth.urls import router as auth_router


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