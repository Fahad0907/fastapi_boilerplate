from fastapi import APIRouter
from auth.schemas.auth_schema import AuthResponse
from auth.apis import register, login, get_user_profile

router = APIRouter(prefix="/auth", tags=["auth"])

# Register routes using function-based views with service layer
router.post("/register", response_model=AuthResponse, status_code=201)(register)
router.post("/login")(login)
router.get("/profile/{user_id}", response_model=AuthResponse)(get_user_profile)
