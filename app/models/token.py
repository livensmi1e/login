from pydantic import BaseModel

from models.response import Response

from enum import Enum

from typing import Optional

from datetime import datetime

from uuid import UUID

class Token(BaseModel):
    access_token: str

class TokenResponse(Response):
    data: Token

class Verify(BaseModel):
    is_valid: bool

class VerifyResponse(Response):
    data: Verify

class SessionStatus(Enum):
    ACTIVE = "active"
    LEAVE = "leave"

class CreateSession(BaseModel):
    ip: str
    location: str
    user_agent: str
    user_id: UUID
    status: SessionStatus
    token: str

class SessionModel(CreateSession):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

class UpdateSession(BaseModel):
    status: Optional[SessionStatus] = SessionStatus.LEAVE
    token: Optional[str] = None

class SetCookie(BaseModel):
    access_token: str
    session_id: str

class SetCookieResponse(Response):
    data: SetCookie