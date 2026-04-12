# Docker Setup Guide

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Setup with Docker

1. **Clone/Copy the .env file**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Update .env with your desired passwords
   ```

2. **Build and Start Docker Containers**
   ```bash
   docker-compose up -d --build
   ```

3. **Check Services**
   ```bash
   # Check if containers are running
   docker-compose ps
   
   # View logs
   docker-compose logs -f fastapi
   docker-compose logs -f postgres
   ```

4. **Access Your Application**
   - FastAPI App: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Database Migrations with Alembic

#### First Time Setup (Create Initial Migration)
```bash
# Create the initial migration from your models
docker-compose exec fastapi alembic revision --autogenerate -m "Initial migration"
```

#### Run Migrations
```bash
# Automatically runs on container startup, or manually:
docker-compose exec fastapi alembic upgrade head
```

#### View Migration History
```bash
docker-compose exec fastapi alembic history
```

#### Downgrade (if needed)
```bash
docker-compose exec fastapi alembic downgrade -1
```

### Common Docker Commands

```bash
# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Rebuild images
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v

# Execute command in container
docker-compose exec fastapi bash

# View database
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
```

### Environment Variables

Edit `.env` file with your configuration:

```env
# Database Configuration
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=fastapi_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# API Configuration
API_PORT=8000

# SQLAlchemy Database URL
DATABASE_URL=postgresql+asyncpg://fastapi_user:your_secure_password@postgres:5432/fastapi_db

# JWT Configuration (optional)
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### PostgreSQL Connection Details

- **Host**: `postgres` (inside Docker network) or `localhost` (from host machine)
- **Port**: `5432`
- **Database**: Set via `POSTGRES_DB` in `.env`
- **Username**: Set via `POSTGRES_USER` in `.env`
- **Password**: Set via `POSTGRES_PASSWORD` in `.env`

### Local Development without Docker

If you want to run locally without Docker:

1. **Install PostgreSQL** (macOS):
   ```bash
   # Using Homebrew
   brew install postgresql@16
   brew services start postgresql@16
   ```

2. **Create a Local Database**
   ```bash
   psql postgres
   CREATE USER fastapi_user WITH PASSWORD 'password';
   CREATE DATABASE fastapi_db OWNER fastapi_user;
   ```

3. **Update .env**
   ```env
   DATABASE_URL=postgresql+asyncpg://fastapi_user:password@localhost:5432/fastapi_db
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

6. **Run the App**
   ```bash
   uvicorn main:app --reload
   ```

### Troubleshooting

**Port already in use**
```bash
# Change port in .env
API_PORT=8001
```

**Database connection refused**
```bash
# Wait for Postgres to be healthy
docker-compose logs postgres
# Should see "database system is ready to accept connections"
```

**Migration errors**
```bash
# Check migration history
docker-compose exec fastapi alembic history

# Downgrade if needed
docker-compose exec fastapi alembic downgrade base

# Remove and recreate containers
docker-compose down -v
docker-compose up -d --build
```

**Permission denied on .venv**
```bash
# Rebuild with proper permissions
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### Production Considerations

For production deployment:

1. **Use strong passwords** in `.env`
2. **Set `DEBUG=False`** (Not currently used, but good practice)
3. **Use `--reload` off** in production (already disabled in entrypoint.sh)
4. **Use a proper database backup strategy**
5. **Use separate docker-compose files** for production (`docker-compose.prod.yml`)
6. **Use environment-specific .env files**
7. **Set up proper logging and monitoring**

### Docker Image Details

- **Python**: 3.11-slim (minimal, efficient)
- **Multi-stage build**: Reduces final image size
- **Async support**: AsyncPG for PostgreSQL, async SQLAlchemy
- **Auto-migration**: Alembic runs on container startup
