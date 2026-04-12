# Quick Start Guide

## One-Command Setup

```bash
bash setup-docker.sh
```

## Manual Setup

### 1. Configure Environment
```bash
cp .env.example .env
# Edit .env with your passwords (optional for dev)
```

### 2. Start Containers
```bash
docker-compose up -d --build
```

### 3. Create Initial Migration
Wait for PostgreSQL to be ready (check logs), then:
```bash
docker-compose exec fastapi alembic revision --autogenerate -m "Initial migration"
```

### 4. Access Application
- **App**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## File Structure

```
.
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # PostgreSQL + FastAPI services
├── .env                    # Environment variables (dev)
├── .env.example           # Template for environment vars
├── alembic/               # Database migrations
│   ├── versions/          # Migration files
│   ├── env.py            # Migration configuration
│   └── script.py.mako    # Migration template
├── alembic.ini           # Alembic config file
├── entrypoint.sh         # Container startup script
└── requirements.txt      # Python dependencies (updated)
```

## Key Technologies

- **FastAPI**: Async web framework
- **PostgreSQL**: Relational database
- **SQLAlchemy**: Async ORM
- **Alembic**: Database migration tool
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

## Common Tasks

### View Logs
```bash
docker-compose logs -f fastapi
docker-compose logs -f postgres
```

### Access PostgreSQL
```bash
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
```

### Create New Migration
```bash
docker-compose exec fastapi alembic revision --autogenerate -m "Description"
```

### Downgrade Migration
```bash
docker-compose exec fastapi alembic downgrade -1
```

### Restart Services
```bash
docker-compose restart
```

### Clean Up
```bash
docker-compose down -v  # Remove volumes too
```

## Troubleshooting

**Issue**: Port already in use
```bash
# Change API_PORT in .env
```

**Issue**: PostgreSQL connection refused
```bash
# Wait for startup, check logs:
docker-compose logs postgres
```

**Issue**: Migration errors
```bash
# Rebuild everything:
docker-compose down -v
docker-compose up -d --build
```

See DOCKER_SETUP.md for detailed documentation.
