from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
from database import get_engine, Base
from auth.urls import router as auth_router
from middlewares import (
    logging_middleware,
    error_middleware,
    http_exception_handler,
    validation_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="FastAPI Practice",
    description="Structured FastAPI application",
    version="1.0.0",
    lifespan=lifespan,
)


# ── 1. Exception handlers ─────────────────────────────────
# registered first — always available regardless of middleware
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


# ── 2. Middleware (add_middleware) ────────────────────────
# added first = runs LAST on request (innermost layer)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "yourdomain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── 3. Custom middleware (@app.middleware) ─────────────────
# added last = runs FIRST on request (outermost layer)
# error handler must be outermost — catches everything below it
@app.middleware("http")
async def add_error_handling(request, call_next):
    return await error_middleware(request, call_next)

# logging wraps everything except error handler
@app.middleware("http")
async def add_logging(request, call_next):
    return await logging_middleware(request, call_next)


# ── 4. Routers ────────────────────────────────────────────
app.include_router(auth_router)


# ── 5. Root route ─────────────────────────────────────────
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI"}