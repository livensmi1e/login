from fastapi import Depends

from repository.user import UserRepo

from models.user import *
from models.token import Token, Verify

from handlers.security import PasswordHashing, TokenHandler

class AuthHandler:
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)) -> None:
        self._repo = user_repo

    def create(self, new_user: CreateUser) -> PublicUser:
        user = self._repo.get(QueryUser(email=new_user.email))
        if user:
            raise Exception("User already exists")
        new_user.password = PasswordHashing().hash(new_user.password)
        user = self._repo.create(new_user)
        return user
    
    def login(self, loggin_user: LoginUser) -> UserModel:
        user = self._repo.get_internal(QueryUser(email=loggin_user.email))
        if not user:
            raise Exception("Your crenedtials are incorrect")
        if not PasswordHashing().verify_password(loggin_user.password, user.password):
            raise Exception("Your credentials are incorrect")
        return Token(
            access_token=TokenHandler().gen_token(str(user.id))
        )
    
    def verify(self, token: str) -> Verify:
        return Verify(
            is_valid=TokenHandler().verify_token(token)
        )