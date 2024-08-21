from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from repository.user import UserRepo

from models.user import InternalUser, QueryUser, PublicUser

from handlers.security import TokenHandler

from typing import Annotated

security = HTTPBearer(scheme_name="Bearer")

class UserContext:
    def __init__(
        self,
        auth_header: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        repo: UserRepo = Depends(UserRepo),
        jwt: TokenHandler = Depends(TokenHandler)
    ):
        self._token = auth_header.credentials
        if not jwt.verify_token(self._token):
            raise Exception("Token is invalid or expired")
        id = jwt.payload(self._token)["sub"]["user_id"]
        self._user = repo.get(QueryUser(id=id))
        if not self._user:
            raise Exception("Token is invalid or expired")

    def user(self) -> PublicUser:
        return self._user
    
