from fastapi import Request
from fastapi_cache.decorator import cache
from app.templates_cache_coder import TemplatesCoder
from app.templates import templates
from app.getenv import is_production


@cache(expire=30, namespace='server-health', coder=TemplatesCoder)
async def homepage_route(request: Request):
    return templates.TemplateResponse('index.html', {
        'request': request,
        'is_production': is_production
    })
