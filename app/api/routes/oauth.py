from fastapi import APIRouter, Depends, HTTPException, Response as FastAPIResponse

from utils.http import APIResponse

from models.oauth import OauthRequest, OauthResponse, OauthTokenRequest
from models.token import TokenResponse

from handlers.oauth import OauthHandler

router = APIRouter()

@router.post("/oauth2", response_model=OauthResponse)
async def oauth(
    oauth_req: OauthRequest,
    oauth_handler: OauthHandler = Depends(OauthHandler)
):
    try:
        auth_res: OauthResponse = oauth_handler.get_oauth(oauth_req)
        return APIResponse.success(200, "Authorization request created successful", auth_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/oauth2/callback", response_model=TokenResponse)
async def oauth_login(
    token_req: OauthTokenRequest,
    response: FastAPIResponse,
    oauth_handler: OauthHandler = Depends(OauthHandler)
):
    try:
        session_id, token = oauth_handler.exchange_key(token_req)
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=1800)
        response.set_cookie(key="auth", value=token.access_token, httponly=True, max_age=1800)
        return APIResponse.success(200, "Login successful", token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))