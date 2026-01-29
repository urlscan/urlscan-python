import pytest
from pytest_httpserver import HTTPServer

from urlscan import Client, Pro


@pytest.fixture
def api_key():
    return "dummy"


@pytest.fixture
def client(httpserver: HTTPServer, api_key: str):
    with Client(
        api_key=api_key, base_url=f"http://{httpserver.host}:{httpserver.port}"
    ) as client:
        yield client


@pytest.fixture
def pro(httpserver: HTTPServer, api_key: str):
    with Pro(
        api_key=api_key, base_url=f"http://{httpserver.host}:{httpserver.port}"
    ) as client:
        yield client
