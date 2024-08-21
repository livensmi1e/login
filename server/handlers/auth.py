from fastapi import Depends

from repository.user import UserRepo

from models.user import *

from handlers.security import PasswordHashing

class AuthHandler:
    def __init__(self, user_repo: UserRepo = Depends(UserRepo)) -> None:
        self._repo = user_repo

    def create(self, new_user: CreateUser) -> UserModel:
        user = self._repo.get_by_email(new_user.email)
        if user:
            raise Exception("User already exists")
        new_user.password = PasswordHashing().hash(new_user.password)
        user = self._repo.create(new_user)
        return user