import os

class Crypto:
    @staticmethod
    def gen_secret() -> bytes:
        return os.urandom(32)