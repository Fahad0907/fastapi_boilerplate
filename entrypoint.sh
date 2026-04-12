#!/bin/bash
set -e

echo "Starting FastAPI Application..."
echo "================================"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "PostgreSQL is ready!"
echo ""

# Run Alembic migrations
echo "Running database migrations..."
alembic upgrade head
echo "Migrations completed!"
echo ""

# Start the FastAPI application
echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
