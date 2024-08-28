from fastapi import APIRouter, Depends, HTTPException

from utils.http import APIResponse

from models.oauth import OauthRequest, OauthResponse

from handlers.oauth import OauthHandler

router = APIRouter()

@router.post("/oauth2", response_model=OauthResponse)
async def oauth(
    oauth_req: OauthRequest,
    oauth_handler: OauthHandler = Depends(OauthHandler)
):
    try:
        auth_res: OauthResponse = oauth_handler.get_oauth(oauth_req)
        return APIResponse.success(200, "Authorization code created successful", auth_res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))