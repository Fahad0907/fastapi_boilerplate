# FastAPI Project Structure

## Overview
Clean, modular, production-ready architecture with proper separation of concerns using FastAPI routers.

## Project Structure

```
fastapi_practice/
├── auth/                          # Authentication module
│   ├── __init__.py
│   ├── router.py                  # Auth endpoints (register, login)
│   ├── utils.py                   # Password hashing, JWT token creation
│   ├── models/
│   │   ├── __init__.py
│   │   └── auth_model.py          # AuthModel ORM model
│   └── schemas/
│       ├── __init__.py
│       └── auth_schema.py         # Pydantic schemas (AuthCreate, AuthResponse)
│
├── routes/                        # API route handlers
│   ├── __init__.py
│   ├── items.py                   # Item endpoints
│   ├── users.py                   # User endpoints
│   └── posts.py                   # Post endpoints
│
├── models/                        # Database models organized by resource
│   ├── __init__.py
│   ├── item_model.py              # Item model
│   ├── user_model.py              # User model
│   └── post_model.py              # Post model
│
├── schemas/                       # Pydantic schemas organized by resource
│   ├── __init__.py
│   ├── item_schema.py             # Item schemas
│   ├── user_schema.py             # User schemas
│   └── post_schema.py             # Post schemas
│
├── main.py                        # Clean FastAPI app & router registration (NO ENDPOINTS)
├── database.py                    # Database configuration
└── README.md                      # This file
```

## Key Design Principles

✅ **Clean main.py** - Only app initialization and router registration (no endpoints)
✅ **Organized Models** - Each model in separate file within `models/` folder
✅ **Organized Schemas** - Each schema in separate file within `schemas/` folder  
✅ **Modular Auth** - Complete auth module with models, schemas, and utilities
✅ **Router-based** - Each resource has its own router file
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
