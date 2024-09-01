from pydantic import BaseModel

from models.response import Response

from typing import Optional

class OauthRequest(BaseModel):
    provider: str
    client_url: str

class AuthURL(BaseModel):
    url: str

class OauthResponse(Response):
    data: AuthURL

class OauthTokenRequest(BaseModel):
    code: str
    state: str
    error: Optional[str] = None
    error_description: Optional[str] = None

class OauthTokenParam(BaseModel):
    client_id: str
    client_secret: str
    code: str
    redirect_uri: str
    grant_type: str = "authorization_code"
    code_verifier: Optional[str] = None

    userinfo_url: str
    token_url: str
    headers: dict = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

