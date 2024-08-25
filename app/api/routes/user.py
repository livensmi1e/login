from fastapi import APIRouter, Depends, HTTPException

from models.user import UserResponse

from handlers.auth import AuthMiddleware

from utils.http import APIResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_info(auth_ctx: AuthMiddleware = Depends(AuthMiddleware)):
    try:
        return APIResponse.success(200, "User retrieved successfully", auth_ctx.user())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))