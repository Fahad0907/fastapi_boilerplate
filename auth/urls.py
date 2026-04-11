from fastapi import APIRouter
from auth.schemas.auth_schema import AuthResponse
from auth import views

router = APIRouter(prefix="/auth", tags=["auth"])

# Register routes using function-based views with service layer
router.post("/register", response_model=AuthResponse, status_code=201)(views.register)
router.post("/login")(views.login)
router.get("/profile/{user_id}", response_model=AuthResponse)(views.get_user_profile)
