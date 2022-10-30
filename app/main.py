import rollbar
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.middleware.auth_middleware import auth_middleware
from app.brainly_api.exceptions import BrainlyAPIRequestGeneralException
from app.errors.http_exception import http_exception_handler
from app.errors.brainly_error import brainly_request_error_handler
from app.errors.server_error import internal_error_handler
from app.getenv import env, is_production
from app.routes import tasks, users, ranking, feed, homepage, moderators, reported_content
from app.generate_openapi import generate_custom_openapi


rollbar.init(env('ROLLBAR_ACCESS_TOKEN'))


def on_startup():
    FastAPICache.init(InMemoryBackend())


def get_application() -> FastAPI:
    print(f"Starting the application, is production: {is_production}")

    application = FastAPI(
        title=env('APP_NAME'),
        version=env('APP_VERSION'),
        debug=is_production is False,
        dependencies=[Depends(auth_middleware)],
        docs_url='/documentation',
        openapi_url='/documentation/openapi',
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.add_event_handler('startup', on_startup)

    application.add_exception_handler(HTTPException, http_exception_handler)
    application.add_exception_handler(BrainlyAPIRequestGeneralException, brainly_request_error_handler)
    application.add_exception_handler(Exception, internal_error_handler)

    application.include_router(tasks.router)
    application.include_router(users.router)
    application.include_router(ranking.router)
    application.include_router(feed.router)
    application.include_router(moderators.router)
    application.include_router(reported_content.router)
    application.add_api_route('/', homepage.homepage_route)

    application.openapi_schema = generate_custom_openapi(application)

    return application


app = get_application()
