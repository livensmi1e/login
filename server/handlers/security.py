import hashlib
import jwt

from datetime import datetime, timedelta

import os

from config import settings

from repository.session import SessionRepo

from models.token import SessionModel, CreateSession, UpdateSession

from fastapi import Depends, HTTPException, Header, Request

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

    def gen_token(self, payload: dict, secret: str) -> str:
        now = datetime.now()
        exp = now.__add__(timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE))
        payload.update({
            "exp": exp.timestamp(),
            "iss": settings.PROJECT_NAME,
            "iat": now.timestamp()
        })
        return jwt.encode(payload, secret, algorithm=self._algorithm)

    def verify_token(self, token: str, secret: str) -> bool:
        try:
            jwt.decode(token, secret, algorithms=[self._algorithm])
            return True
        except Exception:
            return False
        
    def payload(self, token: str) -> dict:
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except Exception:
            return {}
    

class UserSession:
    def __init__(
        self, 
        request: Request,
        session_repo: SessionRepo = Depends(SessionRepo),
        user_agent: str = Header(None, alias="User-Agent")
    ) -> None:
        self.repo = session_repo
        self.ua = user_agent
        self.ip = request.client.host