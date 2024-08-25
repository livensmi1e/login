from pydantic import BaseModel, EmailStr

class RecoverRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    password: str
    token: str