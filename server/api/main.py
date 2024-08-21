from fastapi import APIRouter

from api.routes import auth, user, session

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["user"])
api_router.include_router(session.router, prefix="/sessions", tags=["session"])
