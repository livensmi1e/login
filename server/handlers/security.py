import hashlib
import jwt

from datetime import datetime, timedelta

import os

from config import settings

from typing import Annotated, Any

from repository.session import SessionRepo
from repository.user import UserRepo

from models.user import QueryUser, PublicUser
from models.token import SessionModel, CreateSession, UpdateSession

from fastapi import Depends, HTTPException, Header, Request, Cookie
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

class CryptoUtils:
    @staticmethod
    def gen_secret() -> bytes:
        return os.urandom(32)


class PasswordHashing:
    def __init__(self):
        self._algorithm = settings.PASSWORD_ALGORITHM
        self._salt = CryptoUtils.gen_secret()
        self._INTERATIONS = settings.PASSWORD_INTERATIONS

    def hash(self, password: str) -> str:
        return (hashlib.pbkdf2_hmac(
            self._algorithm,
            password.encode(),
            self._salt,
            self._INTERATIONS
        ).hex() + "." + self._salt.hex())
    
    def verify_password(self, raw_pass: str, enc_pass: str) -> bool:
        _, salt = enc_pass.split(".")
        self._salt = bytes.fromhex(salt)
        return enc_pass == self.hash(raw_pass)
    
    def get_salt(self) -> str:
        return self._salt.hex()
    
class SessionHandler:
    def __init__(
        self,
        repo: SessionRepo = Depends(SessionRepo)
    ) -> None:
        self._repo = repo
    
    def get_value(self, key: str) -> str | None:
        return self._repo.get_value(key)
    
    def set_value(self, key: str, value: str, exp) -> None:
        self._repo.set_value(key, value, exp)

    def delete_value(self, key: str) -> None:
        self._repo.delete_value(key)

    def query_session(self, id: str) -> SessionModel | None:
        self._repo.query_session(id)

    def create_session(self, session: CreateSession) -> SessionModel:
        sessionDB = self._repo.create_session(session)
        if not sessionDB:
            raise HTTPException(status_code=500, detail="Session creation failed")
        return sessionDB
    
    def update_session(self, id: str, session: UpdateSession) -> SessionModel:
        session = self._repo.update_session(id, session)
        return session
    
    
class TokenHandler:
    def __init__(self) -> None:
        self._algorithm = settings.TOKEN_ALGORITHM

    def gen_token(self, id: str, secret: str) -> str:
        now = datetime.now()
        exp = now.__add__(timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE))
        payload: dict = {
            "sub": {"user_id": id},
            "exp": exp.timestamp(),
            "iss": settings.PROJECT_NAME,
            "iat": now.timestamp()
        }
        return jwt.encode(payload, secret, algorithm=self._algorithm)

    def verify_token(self, token: str) -> bool:
        try:
            sc = "23f224739753d31221e46eb7524c2514c3a05338580816ad5a2d49c7a25e327c"
            jwt.decode(token, sc, algorithms=[self._algorithm])
            return True
        except Exception:
            return False
        
    def payload(self, token: str) -> dict:
        return jwt.decode(token, options={"verify_signature": False})
    

class UserSession:
    def __init__(
        self, 
        request: Request,
        session_handler: SessionHandler = Depends(SessionHandler),
        user_agent: str = Header(None, alias="User-Agent")
    ) -> None:
        self.handler = session_handler
        self.ua = user_agent
        self.ip = request.client.host


    

security = HTTPBearer(scheme_name="Bearer")

class UserContext:
    def __init__(
        self,
        auth_header: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        auth_cookie: str = Cookie(None, alias="auth"),
        repo: UserRepo = Depends(UserRepo),
        jwt: TokenHandler = Depends(TokenHandler)
    ):
        self._token = auth_header.credentials or auth_cookie
        print(self._token)
        if not jwt.verify_token(self._token):
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
        id = jwt.payload(self._token)["sub"]["user_id"]
        self._user = repo.get(QueryUser(id=id))
        if not self._user:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")

    def user(self) -> PublicUser:
        return self._user