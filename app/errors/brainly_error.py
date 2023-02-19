from http import HTTPStatus
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.brainly_api.exceptions import BrainlyAPIRequestGeneralException
from app.capture_exception import capture_exception_with_request


async def brainly_request_error_handler(
    req: Request,
    exc: BrainlyAPIRequestGeneralException
) -> JSONResponse:
    capture_exception_with_request(exc, req)

    error_source = exc.source
    error_details = exc.error_details

    if error_source == "graphql" and isinstance(error_details, list):
        error_details = [x["message"] for x in error_details]
    elif error_source == "legacy_api":
        error_details = {
            "message": error_details.get("message"),
            "type": error_details.get("exception_type"),
            "protocol_version": int(error_details.get("protocol"))
        }

    return JSONResponse({
        "detail": "brainly_request_error",
        "exception_details": error_details,
        "exception_source": error_source
    }, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
