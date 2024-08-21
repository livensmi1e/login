import hashlib
import jwt

from datetime import datetime, timedelta

from utils.crypto import Crypto

from config import settings

class PasswordHashing:
    def __init__(self):
        self._algorithm = "sha256"
        self._salt = Crypto.gen_secret()
        self._INTERATIONS = 100_000

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
    
class TokenHandler:
    def __init__(self):
        self._algorithm = "HS256"

    def gen_token(self, id: str) -> str:
        now = datetime.now()
        exp = now.__add__(timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE))
        payload: dict = {
            "sub": {"user_id": id},
            "exp": exp.timestamp(),
            "iss": settings.PROJECT_NAME,
            "iat": now.timestamp()
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=self._algorithm)
    
    def verify_token(self, token: str) -> bool:
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=[self._algorithm])
            return True
        except Exception:
            return False
        
    def payload(self, token: str) -> dict:
        return jwt.decode(token, options={"verify_signature": False})