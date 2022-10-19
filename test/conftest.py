import pytest
from starlette.testclient import TestClient

from app.main import app
from .secret_constants import AUTH_HEADER


def get_test_app():
    client = TestClient(app)

    client.headers = {
        'authorization': AUTH_HEADER
    }

    return client


@pytest.fixture(scope='module')
def test_app():
    yield get_test_app()
