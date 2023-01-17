import logging
from http import HTTPStatus
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.capture_exception import capture_exception_with_request


async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    capture_exception_with_request(exc, request)

    logging.error(exc)

    return JSONResponse({
        "detail": "internal_server_error"
    }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
