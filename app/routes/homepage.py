from fastapi import Request
from app.templates import templates
from app.getenv import is_production


async def homepage_route(request: Request):
    return templates.TemplateResponse('index.html', context={
        'request': request,
        'is_production': is_production
    })
