import logging
from typing import Any
from abc import ABC
from http import HTTPStatus
from httpx import AsyncClient as HttpClient
from app.getenv import env
from .exceptions import BrainlyAPIRequestGeneralException


MAX_BODY_LENGTH_IN_LOG = 400


class Api(ABC):
    auth_token = env("BRAINLY_AUTH_TOKEN")
    legacy_api_url = f"{env('BRAINLY_LEGACY_API_HOST')}/api/28"
    graphql_api_url = env("BRAINLY_GRAPHQL_API_URL")

    _client: HttpClient

    def __init__(self):
        self._client = HttpClient(
            headers={
                "x-b-token-long": self.auth_token,
                "x-service-name": "znanija_api_gateway_backend"
            },
            cookies={"Zadanepl_cookie[Token][Long]": self.auth_token},
            timeout=25,
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
        """Make a request to the specified `url` on the Brainly market"""
        try:
            r = await self._client.request(method, url, json=body)

            # Log the request
            body_in_log = str(body)
            if len(body_in_log) > MAX_BODY_LENGTH_IN_LOG:
                body_in_log = f"{body_in_log[:MAX_BODY_LENGTH_IN_LOG]}..."

            logging.info(f"Brainly API request -> {r.status_code} {r.url.path}, body: {body_in_log}")

            assert r.status_code != HTTPStatus.BAD_GATEWAY, f"the response status is {r.status_code}"
            if r.status_code == HTTPStatus.FORBIDDEN and "captcha" in r.text:
                raise ValueError("403 Forbidden error")

            return r.json()
        except Exception as exc:
            raise BrainlyAPIRequestGeneralException(str(exc))
