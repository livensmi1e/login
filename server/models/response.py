from pydantic import BaseModel

from typing import Any

class Response(BaseModel):
    status_code: int = 200
    message: str
    data: BaseModel

class ErrorResponse(BaseModel):
    status_code: int = 500
    message: str
    error: Any