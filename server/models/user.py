from pydantic import BaseModel, EmailStr

from datetime import datetime
from uuid import UUID

from typing import Optional

from models.response import Response

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserModel(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class PublicUser(UserModel):
    pass

class InternalUser(BaseModel):
    id: UUID
    email: EmailStr
    password: str

class QueryUser(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(Response):
    data: PublicUser
