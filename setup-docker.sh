#!/bin/bash
set -e

echo "FastAPI Docker Setup Script"
echo "=========================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env created"
    echo ""
    echo "⚠️  Please update .env with your desired passwords and secrets"
    echo "   Edit .env before running docker-compose"
    exit 0
fi

echo "✓ .env file found"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    exit 1
fi

echo "✓ Docker found"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    exit 1
fi

echo "✓ Docker Compose found"
echo ""

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

echo ""
echo "✓ Containers started!"
echo ""
echo "Next steps:"
echo "1. Wait a few seconds for PostgreSQL to be ready"
echo "2. Create initial migration:"
echo "   docker-compose exec fastapi alembic revision --autogenerate -m 'Initial migration'"
echo "3. View your app at: http://localhost:8000"
echo "4. View API docs at: http://localhost:8000/docs"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
