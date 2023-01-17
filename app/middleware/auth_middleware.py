import base64
from fastapi import Header, HTTPException
from app.getenv import env


async def auth_middleware(authorization: str | None = Header(default=None)):
    AUTH_USER = env("AUTH_USER")
    AUTH_PASS = env("AUTH_PASSWORD")

    try:
        assert authorization is not None

        auth_token = authorization.split(" ").pop()
        auth_data = base64.b64decode(auth_token).decode("utf-8").split(":")

        assert auth_data[0] == AUTH_USER and auth_data[1] == AUTH_PASS
    except (AssertionError, UnicodeDecodeError):
        raise HTTPException(
            status_code=401,
            detail="not_authed",
            headers={
                "WWW-Authenticate": "Basic realm=\"Znanija Tools\", charset=\"UTF-8\""
            }
        )
