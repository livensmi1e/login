from fastapi import APIRouter, Depends, HTTPException

from utils.http import APIResponse

from models.response import Response
from models.user import CreateUser, UserResponse, LoginUser
from models.token import TokenResponse, VerifyResponse, Token

from handlers.auth import AuthHandler

router = APIRouter()

@router.get("/", response_model=Response)
async def example():
    try:
        return APIResponse.success(
            "200", 
            "Hello, World!"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/register", response_model=UserResponse)
async def register(new_user: CreateUser, auth_handler: AuthHandler = Depends(AuthHandler)):
    try:
        user = auth_handler.create(new_user)
        return APIResponse.success(201, "User created successfully", user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginUser, auth_handler: AuthHandler = Depends(AuthHandler)):
    try:
        token = auth_handler.login(user)
        return APIResponse.success(200, "Login successful", token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/verify", response_model=VerifyResponse)
async def verify(token: Token, auth_handler: AuthHandler = Depends(AuthHandler)):
    try:
        verified = auth_handler.verify(token.access_token)
        return APIResponse.success(200, "Token verified", verified)
    except Exception:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
