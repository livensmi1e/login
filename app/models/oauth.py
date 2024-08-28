from pydantic import BaseModel

from models.response import Response

class OauthRequest(BaseModel):
    provider: str
    client_url: str

class AuthURL(BaseModel):
    url: str

class OauthResponse(Response):
    data: AuthURL


