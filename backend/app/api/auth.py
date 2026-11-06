from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.progress_service import progress_service, UserProfileDTO

router = APIRouter(prefix="/api/auth", tags=["Authentication & User Profiles"])


class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = "password"


class SignupRequest(BaseModel):
    name: str
    email: str
    password: Optional[str] = "password"


class AuthResponse(BaseModel):
    token: str
    user: UserProfileDTO


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest) -> AuthResponse:
    """Authenticates user and returns session token and profile."""
    if not payload.email or not payload.email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address cannot be empty.",
        )
    name = payload.email.split("@")[0].replace(".", " ").title()
    user = progress_service.authenticate_demo(email=payload.email.strip(), name=name)
    return AuthResponse(token="sqlforge-session-token-demo", user=user)


@router.post("/signup", response_model=AuthResponse)
def signup(payload: SignupRequest) -> AuthResponse:
    """Registers a new user and returns authenticated session."""
    if not payload.email or not payload.email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email address cannot be empty.",
        )
    if not payload.name or not payload.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name cannot be empty.",
        )
    user = progress_service.authenticate_demo(email=payload.email.strip(), name=payload.name.strip())
    return AuthResponse(token="sqlforge-session-token-demo", user=user)


@router.post("/logout")
def logout() -> Dict[str, str]:
    """Terminates active session."""
    return {"message": "Successfully logged out."}


@router.get("/me", response_model=UserProfileDTO)
def get_current_user() -> UserProfileDTO:
    """Retrieves authenticated user profile with streak, XP, and rank title."""
    return progress_service.get_current_user_dto()

