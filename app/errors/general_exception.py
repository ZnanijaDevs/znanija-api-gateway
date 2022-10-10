from starlette.requests import Request
from starlette.responses import JSONResponse
from app.capture_exception import capture_exception_with_request


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    capture_exception_with_request(exc, request)

    return JSONResponse({
        'detail': 'internal_server_error',
        'status': 500
    }, status_code=500)
