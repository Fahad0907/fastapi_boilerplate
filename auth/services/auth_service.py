from fastapi import HTTPException, status
from ..repositories.auth_repositories import AuthRepository
from ..utils import PasswordHasher, TokenManager
from auth.models.auth_model import AuthModel
from ..schemas.auth_schema import AuthCreate


class AuthService:
    """Responsibility: Handle authentication business logic."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
        self.password_hasher = PasswordHasher()
        self.token_manager = TokenManager()
    
    async def register_user(self, auth_data: AuthCreate) -> AuthModel:
        # Check if user exists
        if await self.repository.user_exists(auth_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Hash password
        hashed_password = self.password_hasher.hash(auth_data.password)
        
        # Create user
        return await self.repository.create_user(auth_data.username, hashed_password)
    
    async def authenticate_user(self, username: str, password: str) -> AuthModel:
        # Get user
        user = await self.repository.get_user_by_username(username)
        
        # Validate user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Validate password
        if not self.password_hasher.verify(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        return user
    
    def generate_auth_token(self, user_id: int) -> str:
        """Generate access token for authenticated user."""
        return self.token_manager.create_access_token(data={"user_id": user_id})
    
    async def get_user_profile(self, user_id: int) -> AuthModel:
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user