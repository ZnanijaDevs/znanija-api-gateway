import logging
import rollbar
from starlette.requests import Request
from .getenv import is_production


def capture_exception_with_request(exc: Exception, request: Request):
    """Capture the exception and send to Rollbar"""
    logging.exception(exc)

    if is_production:
        rollbar.report_exc_info(request=request)
