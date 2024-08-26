from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.response import *

class APIResponse:
    @staticmethod
    def success(status_code: int, message: str, data: dict = {}) -> Response:
        res = Response(
            status_code=status_code,
            message=message,
            data=data
        )
        return JSONResponse(content=jsonable_encoder(res), status_code=status_code)
    
    @staticmethod
    def error(status_code: int, message: str, error: any) -> JSONResponse:
        error_response = ErrorResponse(
            status_code=status_code,
            error=Error(
                message=message,
                detail=error
            )
        )
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(error_response)
        )