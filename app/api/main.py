from fastapi import APIRouter

from api.routes import auth, user, session, oauth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(session.router, prefix="/sessions", tags=["session"])
api_router.include_router(oauth.router, tags=["oauth2"])
