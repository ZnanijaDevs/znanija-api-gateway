from http import HTTPStatus


def test_no_auth(test_app):
    del test_app.headers["authorization"]

    response = test_app.get("/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_is_authed(test_app):
    return test_app.get("/").status_code == HTTPStatus.OK
