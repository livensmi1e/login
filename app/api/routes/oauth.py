from fastapi import APIRouter, Depends, HTTPException, Response as FastAPIResponse

from utils.http import APIResponse

from models.oauth import OauthRequest, OauthResponse, OauthTokenRequest
from models.token import SetCookieResponse

from handlers.oauth import OauthHandler

router = APIRouter()

@router.post("/oauth2", response_model=OauthResponse)
async def oauth(
    oauth_req: OauthRequest,
    oauth_handler: OauthHandler = Depends(OauthHandler)
):
    try:
        auth_res: OauthResponse = oauth_handler.get_oauth(oauth_req)
        return APIResponse.success(201, "Authorization request created successful", auth_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/oauth2/callback", response_model=SetCookieResponse)
async def oauth_login(
    token_req: OauthTokenRequest,
    response: FastAPIResponse,
    oauth_handler: OauthHandler = Depends(OauthHandler)
):
    try:
        cookies = oauth_handler.exchange_key(token_req)
        response.set_cookie(
            key="session_id", value=cookies.session_id, httponly=True, max_age=1800, samesite="none", secure=True
        )
        response.set_cookie(
            key="auth", value=cookies.access_token, httponly=True, max_age=1800, samesite="none", secure=True
        )
        return APIResponse.success(200, "Login successful", cookies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))