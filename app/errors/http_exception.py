from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    status_code = exc.status_code

    return JSONResponse(
        content={
            "detail": exc.detail,
            "status": status_code
        },
        status_code=status_code,
        headers=getattr(exc, "headers", None)
    )
