from fastapi import APIRouter, Depends, HTTPException

from models.user import UserResponse

from handlers.user import UserContext

from utils.http import APIResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_info(ctx: UserContext = Depends(UserContext)):
    try:
        return APIResponse.success(200, "User retrieved successfully", ctx.user())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))