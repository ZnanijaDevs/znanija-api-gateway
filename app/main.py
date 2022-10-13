import rollbar
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app.middleware.auth_middleware import auth_middleware
from app.brainly_api.exceptions import BrainlyAPIRequestGeneralException
from app.errors.general_exception import exception_handler
from app.errors.http_exception import http_exception_handler
from app.errors.brainly_error import brainly_request_error_handler
from app.getenv import env, is_production
from app.routes import brainly_tasks, brainly_users, brainly_ranking, homepage


rollbar.init(env('ROLLBAR_ACCESS_TOKEN'))


def get_application() -> FastAPI:
    print(f"Starting the application, is production: {is_production}")

    application = FastAPI(
        name='znanija-tools-server',
        debug=is_production is False,
        dependencies=[Depends(auth_middleware)],
        docs_url=None,
        openapi_url=None
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_exception_handler(Exception, exception_handler)
    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(BrainlyAPIRequestGeneralException, brainly_request_error_handler)

    application.include_router(brainly_tasks.router)
    application.include_router(brainly_users.router)
    application.include_router(brainly_ranking.router)
    application.add_api_route('/', homepage.homepage_route)

    return application


app = get_application()
