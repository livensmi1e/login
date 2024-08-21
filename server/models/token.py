from pydantic import BaseModel

from models.response import Response

class Token(BaseModel):
    access_token: str

class TokenResponse(Response):
    data: Token

class Verify(BaseModel):
    is_valid: bool

class VerifyResponse(Response):
    data: Verify