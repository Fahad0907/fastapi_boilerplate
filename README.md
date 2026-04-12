# FastAPI Practice Project

Production-ready FastAPI application with Docker, PostgreSQL, and Alembic migrations.

## Quick Start

### Docker Setup (Recommended)

```bash
# 1. Setup environment variables
cp .env.example .env

# 2. Build and start containers
docker-compose up -d --build

# 3. Create initial migration (after PostgreSQL starts)
docker-compose exec fastapi alembic revision --autogenerate -m "Initial migration"

# 4. Access the application
# - App: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

Or use the setup script:
```bash
bash setup-docker.sh
```

### Using Make Commands

```bash
make up           # Start containers
make down         # Stop containers
make logs         # View logs
make shell        # Access FastAPI container
make migrate      # Run migrations
make fresh        # Clean rebuild
```

See [QUICKSTART.md](QUICKSTART.md) for more details.

## Project Structure

```
fastapi_practice/
├── auth/                          # Authentication module
│   ├── __init__.py
│   ├── urls.py                    # Auth routes
│   ├── utils.py                   # Password hashing, JWT
│   ├── apis/
│   │   └── auth.py               # Auth endpoints
│   ├── models/
│   │   └── auth_model.py         # Auth ORM model
│   ├── repositories/
│   │   └── auth_repositories.py  # Data access layer
│   ├── schemas/
│   │   └── auth_schema.py        # Pydantic schemas
│   └── services/
│       └── auth_service.py       # Business logic
│
├── main.py                        # FastAPI application
├── database.py                    # SQLAlchemy configuration
├── Dockerfile                     # Container image
├── docker-compose.yml            # Development environment
├── docker-compose.prod.yml       # Production environment
├── alembic.ini                   # Alembic configuration
├── alembic/                      # Database migrations
├── .env                          # Environment variables
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
├── Makefile                      # Common commands
├── QUICKSTART.md                 # Quick start guide
├── DOCKER_SETUP.md              # Docker documentation
└── README.md                     # This file
```

## Technologies

- **FastAPI** - Modern async web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - Async ORM
- **Asyncpg** - Fast async PostgreSQL driver
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **Bcrypt** - Password hashing
- **PyJWT** - JWT tokens
- **Docker** - Containers
- **Docker Compose** - Multi-container orchestration

## Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Key variables:
```env
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/db_name
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=fastapi_db
API_PORT=8000
```

See [.env.example](.env.example) for all available options.

## Database Migrations

### Create a Migration
```bash
# Auto-generate from model changes
docker-compose exec fastapi alembic revision --autogenerate -m "Add users table"
```

### Run Migrations
```bash
# Runs automatically on container startup
# Or manually:
docker-compose exec fastapi alembic upgrade head
```

### View History
```bash
docker-compose exec fastapi alembic history
```

### Downgrade
```bash
docker-compose exec fastapi alembic downgrade -1
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md#database-migrations-with-alembic) for detailed migration guide.

## Development

### Local Without Docker

1. Install PostgreSQL:
   ```bash
   brew install postgresql@16
   brew services start postgresql@16
   ```

2. Create database:
   ```bash
   createdb fastapi_db
   ```

3. Install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   alembic upgrade head
   ```

5. Start app:
   ```bash
   uvicorn main:app --reload
   ```

### With Docker

1. Start containers:
   ```bash
   docker-compose up -d --build
   ```

2. Access shell:
   ```bash
   docker-compose exec fastapi bash
   ```

## Common Tasks

### View Logs
```bash
docker-compose logs -f fastapi        # FastAPI logs
docker-compose logs -f postgres       # Database logs
docker-compose logs -f                # All logs
```

### Access Database
```bash
docker-compose exec postgres psql -U fastapi_user -d fastapi_db
```

### Run Health Check
```bash
bash healthcheck.sh
```

### Clean Up
```bash
docker-compose down        # Stop containers
docker-compose down -v     # Remove containers and data
```

## API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Key Design Principles

✅ **Clean main.py** - Only app initialization and router registration
✅ **Modular structure** - Each feature in its own module
✅ **Async-first** - Full async/await support
✅ **Database migrations** - Version control for schema
✅ **Environment-based config** - Secrets in .env
✅ **Docker-ready** - Development and production setups
✅ **Code organization** - Layers: APIs → Services → Repositories → Models

## Authentication Module

The `auth/` module provides:
- User registration and login
- Password hashing with bcrypt
- JWT token generation
- Protected endpoints
- Role-based access (extensible)

## Production Deployment

For production use `docker-compose.prod.yml`:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Production checklist:
- [ ] Update `.env` with strong passwords
- [ ] Use environment-specific secrets management
- [ ] Enable HTTPS/SSL
- [ ] Setup backup strategy for PostgreSQL
- [ ] Configure logging and monitoring
- [ ] Use managed database service
- [ ] Setup CI/CD pipeline

## Troubleshooting

### Containers won't start
```bash
docker-compose logs              # Check logs
docker-compose down -v           # Clean slate
docker-compose up -d --build     # Rebuild
```

### Database connection errors
```bash
docker-compose logs postgres     # Check DB logs
docker-compose restart postgres  # Restart database
```

### Port already in use
```bash
# Change API_PORT in .env
API_PORT=8001
```

See [DOCKER_SETUP.md](DOCKER_SETUP.md#troubleshooting) for detailed troubleshooting.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## License

MIT

## Overview (Original)
Clean, modular, production-ready architecture with proper separation of concerns using FastAPI routers.
✅ **Easy to Extend** - Add new resources by following the pattern

## Available Endpoints

### Items
- `POST /items/` - Create item
- `GET /items/` - Get paginated items
- `GET /items/{item_id}` - Get single item

### Users
- `POST /users/` - Create user
- `GET /users/{user_id}` - Get single user

### Posts
- `POST /posts/` - Create post
- `GET /posts/{post_id}` - Get single post

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get access token

## Running the Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the server
uvicorn main:app --reload

# API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
```
