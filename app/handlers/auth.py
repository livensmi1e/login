from fastapi import Depends, Cookie, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from repository.user import UserRepo

from models.user import (
    PublicUser,
    CreateUser,
    QueryUser,
    LoginUser,
    UpdateUser
)

from models.token import (
    Token, 
    Verify, 
    SessionStatus, 
    CreateSession, 
    UpdateSession
)

from models.auth import PasswordReset

from handlers.security import (
    PasswordHashing, 
    TokenHandler, 
    UserSession, 
    CryptoUtils
)

from config import settings

from typing import Annotated

from repository.user import UserRepo
from repository.session import SessionRepo

import smtplib, ssl

from utils.email_template import process_template

class AuthHandler:
    def __init__(
        self, 
        user_repo: UserRepo = Depends(UserRepo),
        token_handler: TokenHandler = Depends(TokenHandler),
        user_session: UserSession = Depends(UserSession),
    ) -> None:
        self._repo = user_repo
        self._token_handler = token_handler
        self._user_session = user_session

    def create(self, new_user: CreateUser) -> PublicUser:
        user = self._repo.get(QueryUser(email=new_user.email))
        if user:
            raise Exception("User already exists")
        new_user.password = PasswordHashing().hash(new_user.password)
        user = self._repo.create(new_user)
        return user
    
    def login(self, loggin_user: LoginUser) -> tuple[str, Token]:
        user = self._repo.get_internal(QueryUser(email=loggin_user.email))
        if not user:
            raise Exception("Your crenedtials are incorrect")
        if not PasswordHashing().verify_password(loggin_user.password, user.password):
            raise Exception("Your credentials are incorrect")
        secret = self._user_session.repo.get_value(str(user.id))
        if secret:
            raise Exception("You already logged in")
        secret = CryptoUtils.gen_secret().hex() 
        payload: dict = {
            "sub": {"user_id": str(user.id)}
        }
        token = self._token_handler.gen_token(payload, secret)
        self._user_session.repo.set_value(str(user.id), secret, settings.SESSION_EXPIRE)
        session_info = CreateSession(
            ip=self._user_session.ip,
            location="Unknown",
            user_agent=self._user_session.ua,
            user_id=user.id,
            status=SessionStatus.ACTIVE,
            token=token
        )
        sessionDB = self._user_session.repo.create_session(session_info) 
        return str(sessionDB.id), Token(access_token=token)
    
    def logout(self, user_id: str, id: str) -> None:
        self._user_session.repo.delete_value(user_id)
        updated_info = UpdateSession(status=SessionStatus.LEAVE, token="")
        self._user_session.repo.update_session(id, updated_info)

    def verify(self, token: str) -> Verify:
        user_id = self._token_handler.payload(token).get("sub").get("user_id")
        secret = self._user_session.repo.get_value(user_id)
        return Verify(
            is_valid=self._token_handler.verify_token(token, secret)
        )
    
    def recover(self, email: str) -> None:
        user = self._repo.get(QueryUser(email=email))
        if not user:
            raise Exception("Your email is not registered")
        payload: dict = {
            "sub": {"email": email}
        }
        secret = CryptoUtils.gen_secret().hex()
        token = self._token_handler.gen_token(payload, secret)
        self._user_session.repo.set_value(email, secret, settings.RECOVERY_TOKEN_EXPIRE)
        content: str = f"http://{settings.SERVER_HOST}/reset-password?token={token}"
        self.send_email(email, content)

    def send_email(self, email: str, content: str) -> None:
        email = "baongocrubik2007@gmail.com"
        message = process_template(
            from_email=settings.SMTP_USER,
            to_email=email,
            subject="My Auth Password Recovery",
            content=content
        )
        context = ssl.create_default_context()
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, email, message)

    def reset_password(self, password_reset: PasswordReset) -> None:
        sub = self._token_handler.payload(password_reset.token).get("sub")
        email = sub.get("email") if sub else None
        if not email:
            raise Exception("Recovery token is invalid or expired")
        secret = self._user_session.repo.get_value(email)
        if not self._token_handler.verify_token(password_reset.token, secret):
            raise Exception("Recovery token is invalid or expired")
        user = self._repo.get(QueryUser(email=email))
        if not user:
            raise Exception("Recovery token is invalid or expired")
        update_user = UpdateUser(password=PasswordHashing().hash(password_reset.password))
        self._repo.update(str(user.id), update_user)
                
    
security = HTTPBearer(scheme_name="Bearer", auto_error=False)

class AuthMiddleware:
    def __init__(
        self,
        auth_header: Annotated[HTTPAuthorizationCredentials | None, Depends(security)],
        auth_cookie: str = Cookie(None, alias="auth"),
        user_repo: UserRepo = Depends(UserRepo),
        session_repo: SessionRepo = Depends(SessionRepo),
        jwt: TokenHandler = Depends(TokenHandler)
    ):
        self._token = auth_header.credentials if auth_header else auth_cookie
        sub = jwt.payload(self._token).get("sub") 
        user_id = sub.get("user_id") if sub else None
        if not user_id:
            raise Exception("Token is invalid or expired")
        secret = session_repo.get_value(user_id)
        if not jwt.verify_token(self._token, secret):
            raise Exception("Token is invalid or expired")
        self._user = user_repo.get(QueryUser(id=user_id))
        if not self._user:
            raise Exception("Token is invalid or expired")

    def user(self) -> PublicUser:
        return self._user