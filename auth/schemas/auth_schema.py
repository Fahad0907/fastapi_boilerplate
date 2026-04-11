from pydantic import BaseModel, Field


class AuthCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=128)


class AuthResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
