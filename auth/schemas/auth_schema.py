from pydantic import BaseModel, Field, ConfigDict


class AuthCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=128)


class AuthResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
