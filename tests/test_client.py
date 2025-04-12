import datetime
import json
import tempfile

import pytest
from freezegun.api import FrozenDateTimeFactory
from pytest_httpserver import HTTPServer
from werkzeug import Request, Response

from urlscan import Client
from urlscan.error import RateLimitError, RateLimitRemainingError


@pytest.fixture
def api_key():
    return "dummy"


@pytest.fixture
def client(httpserver: HTTPServer, api_key: str):
    with Client(
        api_key=api_key, base_url=f"http://{httpserver.host}:{httpserver.port}"
    ) as client:
        yield client


def test_get(client: Client, httpserver: HTTPServer):
    data = {"foo": "bar"}
    httpserver.expect_request("/dummy").respond_with_json(data)

    got = client.get("/dummy")
    assert got.json() == data

    # confirm whether the API key is set or not
    last_request, _ = httpserver.log[-1]
    assert last_request.method == "GET"
    assert last_request.headers["API-Key"] == client._api_key


def test_post(client: Client, httpserver: HTTPServer):
    data = {"foo": "bar"}
    httpserver.expect_request(
        "/dummy",
        method="POST",
    ).respond_with_json(data)

    got = client.post("/dummy")
    assert got.json() == data


def test_download(client: Client, httpserver: HTTPServer):
    data = b"foo"
    httpserver.expect_request("/dummy").respond_with_data(data)

    with tempfile.NamedTemporaryFile() as tmp_file:
        client.download("/dummy", tmp_file)  # type: ignore
        tmp_file.seek(0)
        assert tmp_file.read() == data


def test_search(client: Client, httpserver: HTTPServer):
    q = "foo"

    # set first request & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "100"},
    ).respond_with_json(
        {
            "results": [{"sort": [1, "dummy"]}],
            "has_more": True,
        }
    )
    # set second requests & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "100", "search_after": "1,dummy"},
    ).respond_with_json(
        {
            "results": [],
            "has_more": False,
        }
    )

    got = list(client.search(q))
    # it should return 1 result
    assert len(got) == 1
    # but it should make two requests
    assert len(httpserver.log) == 2


def test_retry(client: Client, httpserver: HTTPServer):
    def handler(_: Request):
        # return 429 if it's the first request
        if len(httpserver.log) == 0:
            return Response("", status=429, headers={"X-Rate-Limit-Reset-After": "0"})

        # return 200 for the second request
        return Response("", status=200)

    httpserver.expect_request(
        "/dummy",
        method="GET",
    ).respond_with_handler(handler)

    client._retry = True

    got = client.get("/dummy")
    assert got._res.status_code == 200
    # it should have two requests & responses
    assert len(httpserver.log) == 2


def test_without_retry(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/dummy",
        method="GET",
    ).respond_with_json(
        {"message": "Rate limit exceeded", "status": 429},
        status=429,
    )
    with pytest.raises(RateLimitError):
        client.get_json("/dummy")


@pytest.mark.freeze_time("2020-01-01")
def test_rate_limit_remaining_error(
    client: Client, httpserver: HTTPServer, freezer: FrozenDateTimeFactory
):
    def handler(_: Request):
        utcnow = datetime.datetime.now(datetime.timezone.utc)
        if utcnow.date() == datetime.date(2020, 1, 1):
            return Response(
                json.dumps({}),
                status=200,
                headers={
                    "X-Rate-Limit-Remaining": "0",
                    "X-Rate-Limit-Reset": "2020-01-02T00:00:00.000Z",
                },
            )

        if utcnow.date() == datetime.date(2020, 1, 2):
            return Response(
                json.dumps({}),
                status=200,
                headers={
                    "X-Rate-Limit-Remaining": "0",
                    "X-Rate-Limit-Reset": "2020-01-03T00:00:00.000Z",
                },
            )

        raise ValueError("Unexpected condition")

    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="GET",
    ).respond_with_handler(handler)

    # this updates rate limit memo inside the client
    # - remaining: 0
    # - reset: 2020-01-02T00:00:00Z
    assert client.get_result("dummy") is not None
    # thus next request should raise RateLimitRemainingError
    with pytest.raises(RateLimitRemainingError):
        client.get_result("dummy")

    freezer.move_to("2020-01-02")
    # current time >= reset (2020-01-02T00:00:00Z)
    # so it should not raise RateLimitRemainingError
    assert client.get_result("dummy") is not None
    with pytest.raises(RateLimitRemainingError):
        client.get_result("dummy")
