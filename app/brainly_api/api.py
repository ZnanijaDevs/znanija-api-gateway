from typing import Any
from http import HTTPStatus
from httpx import AsyncClient as HttpClient
from app.getenv import env
from .exceptions import BrainlyAPIRequestGeneralException


class Api:
    auth_token = env('BRAINLY_AUTH_TOKEN')
    legacy_api_url = f"{env('BRAINLY_LEGACY_API_HOST')}/api/28"
    graphql_api_url = env('BRAINLY_GRAPHQL_API_URL')

    _client: HttpClient

    def __init__(self):
        self._client = HttpClient(
            headers={
                'x-b-token-long': self.auth_token,
                'x-service-name': 'znanija_tools_proxy_backend'
            },
            cookies={'Zadanepl_cookie[Token][Long]': self.auth_token},
            timeout=6,
            follow_redirects=False,
            verify=False,
            http2=True
        )

    async def _make_request(
        self,
        url: str,
        method: str,
        body: Any | None = None,
    ):
        try:
            r = await self._client.request(method, url, json=body)

            print(
                '\x1b[1;34m' +
                f"brainly api request -> {url}: body: {body}, auth token: {self.auth_token}" +
                f" // time: {r.elapsed.total_seconds()}s" +
                '\x1b[0m'
            )

            assert r.status_code != HTTPStatus.BAD_GATEWAY, f"the response status is {r.status_code}"

            return r.json()
        except Exception as exc:
            raise BrainlyAPIRequestGeneralException(str(exc))
