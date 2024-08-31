from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from api.main import api_router

from config import settings

from utils.http import APIResponse

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs"
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return APIResponse.error(
        exc.status_code, 
        "Ops! Something went wrong.", 
        exc.detail
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return APIResponse.error(
        status.HTTP_422_UNPROCESSABLE_ENTITY, 
        "Ops! Your request has validation errors.", 
        exc.errors()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_WHITELIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host=settings.SERVER_HOST,
#         port=settings.PORT,
#         log_level="info",
#         reload=True,
#         ssl_keyfile="../certs/key.pem",
#         ssl_certfile="../certs/cert.pem"
#     )