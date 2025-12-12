from fastapi import APIRouter
from app.models.admin import AdminLogin
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin")

@router.post("/login")
def login(data: AdminLogin):
    return AuthService.login(data.email, data.password)
