from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from ..models.auth_model import AuthModel


class AuthRepository:
    """Responsibility: Handle all database operations for auth."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_username(self, username: str) -> Optional[AuthModel]:
        result = await self.db.execute(
            select(AuthModel).filter(AuthModel.username == username)
        )
        return result.scalars().first()
    
    async def get_user_by_id(self, user_id: int) -> Optional[AuthModel]:
        result = await self.db.execute(
            select(AuthModel).filter(AuthModel.id == user_id)
        )
        return result.scalars().first()
    
    async def create_user(self, username: str, hashed_password: str) -> AuthModel:
        db_user = AuthModel(username=username, password=hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user
    
    async def user_exists(self, username: str) -> bool:
        result = await self.db.execute(
            select(AuthModel).filter(AuthModel.username == username)
        )
        return result.scalars().first() is not None