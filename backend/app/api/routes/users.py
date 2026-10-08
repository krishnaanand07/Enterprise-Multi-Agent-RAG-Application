from fastapi import APIRouter, Depends
from app.schemas.auth import UserResponse
from app.api.dependencies import get_current_user
from app.models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get profile details for authenticated user."""
    return UserResponse.model_validate(current_user)
