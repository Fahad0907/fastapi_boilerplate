.PHONY: help build up down logs migrate fresh clean shell db-shell

help:
	@echo "FastAPI Docker Commands"
	@echo "======================="
	@echo "make build              - Build Docker images"
	@echo "make up                 - Start containers"
	@echo "make down               - Stop containers"
	@echo "make logs               - View FastAPI logs"
	@echo "make logs-db            - View PostgreSQL logs"
	@echo "make migrate            - Run Alembic migrations"
	@echo "make migrate-new MSG    - Create new migration (e.g., make migrate-new MSG='Add users table')"
	@echo "make downgrade          - Downgrade last migration"
	@echo "make shell              - Open FastAPI container shell"
	@echo "make db-shell           - Open PostgreSQL shell"
	@echo "make fresh              - Remove containers and volumes, then rebuild"
	@echo "make clean              - Remove containers"
	@echo "make lint               - Run pylint"
	@echo "make format             - Format code with black"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f fastapi

logs-all:
	docker-compose logs -f

logs-db:
	docker-compose logs -f postgres

migrate:
	docker-compose exec fastapi alembic upgrade head

migrate-new:
	@read -p "Enter migration name: " msg; \
	docker-compose exec fastapi alembic revision --autogenerate -m "$$msg"

downgrade:
	docker-compose exec fastapi alembic downgrade -1

shell:
	docker-compose exec fastapi bash

db-shell:
	docker-compose exec postgres psql -U fastapi_user -d fastapi_db

fresh:
	docker-compose down -v
	docker-compose up -d --build

clean:
	docker-compose down

lint:
	docker-compose exec fastapi pylint auth/ main.py database.py

format:
	docker-compose exec fastapi black auth/ main.py database.py

test:
	docker-compose exec fastapi pytest --verbose

ps:
	docker-compose ps

status:
	@echo "Service Status:"
	@docker-compose ps
	@echo ""
	@echo "Database Connection:"
	@docker-compose exec postgres pg_isready -U fastapi_user || echo "PostgreSQL not responding"
	@echo ""
	@echo "API Health:"
	@curl -s http://localhost:8000/docs > /dev/null && echo "✓ API is running" || echo "✗ API is not responding"
