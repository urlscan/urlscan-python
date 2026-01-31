import os

import pytest
from dotenv import load_dotenv

from urlscan import Client, Pro


@pytest.fixture
def api_key() -> str:
    load_dotenv()
    key = os.getenv("URLSCAN_API_KEY")
    assert key
    return key


@pytest.fixture
def client(api_key: str):
    with Client(api_key) as client:
        yield client


@pytest.fixture
def pro(api_key: str):
    with Pro(api_key) as client:
        yield client


@pytest.fixture
def url() -> str:
    return "https://httpbin.org/html"
