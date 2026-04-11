from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from auth.models.auth_model import AuthModel

# Configuration
SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
import os

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

class PasswordHasher:
    """Responsibility: Handle password hashing and verification."""
    
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


class TokenManager:
    """Responsibility: Handle JWT token creation and validation."""
    
    def __init__(self, secret_key: str = None, algorithm: str = "HS256", expire_minutes: int = 30):
        self.secret_key = secret_key or os.getenv("SECRET_KEY", "your-secret-key")
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return {}