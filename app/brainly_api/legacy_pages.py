import json
from typing import Any
from http import HTTPStatus
from base64 import b64decode
from urllib.parse import unquote
from httpx import AsyncClient as HttpClient
from pyquery import PyQuery
from app.getenv import env
from .exceptions import BrainlyAPIRequestGeneralException


http_client = HttpClient(
    base_url=env('BRAINLY_PROXY_HOST_URL'),
    http2=True,
    headers={
        'authorization': f"basic {env('BRAINLY_PROXY_AUTH_PASS')}",
        'x-b-token-long': env('BRAINLY_AUTH_TOKEN'),
    },
    follow_redirects=False,
)


async def _request(path: str, method: str, data: Any | None = None) -> str:
    """Send a request to the legacy page on Znanija.com and returns a text of it"""
    try:
        http_client.cookies.clear()

        response = await http_client.request(method, path, data=data)
        response_text = response.text

        print(f"\033[93m legacy pages request -> {method.upper()} {path}, {data} \033[0m")

        assert response.status_code != HTTPStatus.UNAUTHORIZED, f"{path} 401 Unauthorized error"
        assert response_text != '', 'Invalid token'

        return response_text
    except Exception as exc:
        raise BrainlyAPIRequestGeneralException(str(exc), 'legacy_pages')


async def get_parsed_page(path: str) -> PyQuery:
    """Sends a request to the specified Brainly page, parses it and returns a document"""
    response = await _request(path, 'get')
    return PyQuery(response)


async def get_form_data_from_user_page(user_id: int, form_selector: str) -> dict:
    """Send a request to user profile page, parses it and
    returns the serialized data from the specified form"""
    page = await get_parsed_page(f"/profil/__nick__-{user_id}/solved?limit=1")
    return page(form_selector).serialize_dict()


async def send_form(path: str, form_data: dict | None = None):
    """Send a form data to Brainly"""
    response = await _request(path, 'post', data=form_data)

    infobar_cookie = response.cookies['Zadanepl_cookie[infobar]']
    infobar_cookie = unquote(infobar_cookie)

    messages = json.loads(b64decode(infobar_cookie))

    for message in messages:
        if message['class'] == 'failure':
            raise BrainlyAPIRequestGeneralException(message['text'], 'legacy_pages')
