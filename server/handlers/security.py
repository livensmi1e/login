import hashlib

from utils.crypto import Crypto

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
    
    def verify(self, raw_pass: str, enc_pass: str) -> bool:
        _, salt = enc_pass.split(".")
        return enc_pass == self.hash(raw_pass, salt)