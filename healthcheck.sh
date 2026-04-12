#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "FastAPI Application Health Check"
echo "================================="
echo ""

# Check if containers are running
echo "Checking container status..."
if ! docker-compose ps | grep -q "fastapi_app"; then
    echo -e "${RED}✗ FastAPI container is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ FastAPI container is running${NC}"

if ! docker-compose ps | grep -q "fastapi_postgres"; then
    echo -e "${RED}✗ PostgreSQL container is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ PostgreSQL container is running${NC}"
echo ""

# Check PostgreSQL connection
echo "Checking PostgreSQL connection..."
if docker-compose exec -T postgres pg_isready -U fastapi_user -d fastapi_db > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PostgreSQL is responding${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not responding${NC}"
    exit 1
fi
echo ""

# Check FastAPI health
echo "Checking FastAPI health..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs)
if [ "$HTTP_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ FastAPI is responding (HTTP $HTTP_STATUS)${NC}"
else
    echo -e "${YELLOW}⚠ FastAPI returned HTTP $HTTP_STATUS${NC}"
fi
echo ""

# Check database schema
echo "Checking database tables..."
TABLES=$(docker-compose exec -T postgres psql -U fastapi_user -d fastapi_db -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null)
if [ -n "$TABLES" ]; then
    echo -e "${GREEN}✓ Database has $TABLES tables${NC}"
else
    echo -e "${YELLOW}⚠ Could not read database tables${NC}"
fi
echo ""

# Check migrations
echo "Checking Alembic migrations..."
MIGRATION_COUNT=$(docker-compose exec -T fastapi alembic history 2>/dev/null | wc -l)
if [ "$MIGRATION_COUNT" -gt 0 ]; then
    echo -e "${GREEN}✓ Found $MIGRATION_COUNT migrations${NC}"
else
    echo -e "${YELLOW}⚠ No migrations found${NC}"
fi
echo ""

echo -e "${GREEN}Health check completed!${NC}"
echo ""
echo "Application URLs:"
echo "  - Main app: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
