from pydantic import BaseModel

from typing import Any

class Response(BaseModel):
    status_code: int = 200
    message: str
    data: BaseModel

class Error(BaseModel):
    message: str
    detail: Any

class ErrorResponse(BaseModel):
    status_code: int = 500
    error: Error