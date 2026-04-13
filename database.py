from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# Create engine lazily to avoid issues with greenlets during Alembic migrations
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            future=True,
        )
    return _engine

def get_session_factory():
    return async_sessionmaker(
        get_engine(), class_=AsyncSession, expire_on_commit=False
    )

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    AsyncSessionLocal = get_session_factory()
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()