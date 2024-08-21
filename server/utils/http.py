from fastapi.responses import JSONResponse

from models.response import *

class APIResponse:
    @staticmethod
    def success(status_code: int, message: str, data: dict = {}) -> Response:
        return Response(
            status_code=status_code,
            message=message,
            data=data
        )
    
    @staticmethod
    def error(status_code: int, message: str, error: any) -> JSONResponse:
        error_response = ErrorResponse(
            status_code=status_code,
            message=message,
            error=error
        )
        return JSONResponse(
            status_code=status_code,
            content=error_response.model_dump()
        )