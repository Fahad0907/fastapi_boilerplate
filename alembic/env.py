# Alembic configuration file
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Alembic config object
config = context.config

# Set sqlalchemy.url from environment variable
sqlalchemy_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://fastapi_user:fastapi_password@localhost:5432/fastapi_db"
)
# Convert asyncpg URL to psycopg2 for Alembic (which doesn't support async)
sqlalchemy_url = sqlalchemy_url.replace("postgresql+asyncpg://", "postgresql://")
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# Interpret the config file for Python logging
if config.config_file_name is not None:
    try:
        fileConfig(config.config_file_name)
    except Exception:
        # Logging not configured, skip
        pass

# Add your model's MetaData object for 'autogenerate' support
try:
    from database import Base
    target_metadata = Base.metadata
except Exception:
    # If database import fails, create empty metadata
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
    target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    # Use the converted psycopg2 URL (not asyncpg)
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://fastapi_user:fastapi_password@localhost:5432/fastapi_db"
    ).replace("postgresql+asyncpg://", "postgresql://")
    configuration["sqlalchemy.url"] = db_url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
