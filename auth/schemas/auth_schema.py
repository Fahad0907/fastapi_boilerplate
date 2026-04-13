from pydantic import BaseModel, Field, ConfigDict


class AuthCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=6, max_length=128)
    phone : str = Field(default=None, max_length=20)


class AuthResponse(BaseModel):
    id: int
    username: str
    phone: str | None

    model_config = ConfigDict(from_attributes=True)
