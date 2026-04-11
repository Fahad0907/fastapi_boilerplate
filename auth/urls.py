from fastapi import APIRouter
from auth.schemas.auth_schema import AuthResponse
from auth import views

router = APIRouter(prefix="/auth", tags=["auth"])

# Route definitions (Django style)
router.post("/register", response_model=AuthResponse, status_code=201)(views.register)
router.post("/login")(views.login)
router.get("/me", response_model=AuthResponse)(views.get_current_user_info)
