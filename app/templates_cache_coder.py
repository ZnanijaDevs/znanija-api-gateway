from fastapi_cache.coder import Coder
from starlette.templating import _TemplateResponse as TemplateResponse


class TemplatesCoder(Coder):
    @classmethod
    def encode(cls, value: TemplateResponse):
        return value

    @classmethod
    def decode(cls, value: TemplateResponse):
        return value
