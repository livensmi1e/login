from pydantic import BaseModel, EmailStr

from datetime import datetime
from uuid import UUID

from models.response import Response

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class UserModel(BaseModel):
    id: UUID
    email: EmailStr
    created_at: datetime

class UserResponse(Response):
    data: UserModel

