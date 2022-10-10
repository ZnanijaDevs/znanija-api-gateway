from os.path import dirname
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(f"{dirname(__file__)}/templates")
