from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from auth.models.auth_model import AuthModel
from auth.schemas.auth_schema import AuthCreate, AuthResponse
from auth.services.auth_service import AuthService
from auth.repositories.auth_repositories import AuthRepository


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    """Dependency to inject AuthService."""
    repository = AuthRepository(db)
    return AuthService(repository)


async def register(
    auth_data: AuthCreate,
    service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    """Register a new user."""
    user = await service.register_user(auth_data)
    return AuthResponse.model_validate(user)


async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
) -> dict:
    """Login user and return access token."""
    user = await service.authenticate_user(form_data.username, form_data.password)
    access_token = service.generate_auth_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


async def get_user_profile(
    user_id: int,
    service: AuthService = Depends(get_auth_service)
) -> AuthResponse:
    """Get user profile by user ID."""
    user = await service.get_user_profile(user_id)
    return AuthResponse.model_validate(user)
