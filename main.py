from fastapi import FastAPI
from database import engine, Base
from auth.urls import router as auth_router


app = FastAPI(
    title="FastAPI Practice",
    description="Structured FastAPI application",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# Register routers
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}