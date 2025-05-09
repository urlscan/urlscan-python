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
        {"results": [{"sort": [1, "dummy"]}], "has_more": False, "total": 1}
    )

    got = list(client.search(q))
    # it should return 1 result
    assert len(got) == 1
    # but it should make 1 request
    assert len(httpserver.log) == 1


def test_search_with_iteration_within_10000_results(
    client: Client, httpserver: HTTPServer
):
    q = "foo"

    # set first request & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "1"},
    ).respond_with_json(
        {"results": [{"sort": [1, "dummy"]}], "has_more": False, "total": 2}
    )
    # set second requests & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "1", "search_after": "1,dummy"},
    ).respond_with_json(
        {"results": [{"sort": [2, "dummy"]}], "has_more": False, "total": 2}
    )

    got = list(client.search(q, size=1))
    assert len(got) == 2
    assert len(httpserver.log) == 2


def test_search_with_iteration_over_10000_results(
    client: Client, httpserver: HTTPServer
):
    q = "foo"

    # set first request & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "10000"},
    ).respond_with_json(
        {
            "results": [{"sort": [i, "dummy"]} for i in range(1, 10001)],
            "has_more": True,
            "total": 10000,
        }
    )
    # set second requests & response
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "10000", "search_after": "10000,dummy"},
    ).respond_with_json(
        {
            "results": [
                {"sort": [10001, "dummy"]},
            ],
            "has_more": True,
            "total": 10000,
        }
    )
    # set third requests & response (it stops iteration because of empty results)
    httpserver.expect_request(
        "/api/v1/search/",
        method="GET",
        query_string={"q": q, "size": "10000", "search_after": "10001,dummy"},
    ).respond_with_json(
        {
            "results": [],
            "has_more": True,
            "total": 10000,
        }
    )

    got = list(client.search(q, size=10000))
    assert len(got) == 10001
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
                    "X-Rate-Limit-Action": "retrieve",
                    "X-Rate-Limit-Remaining": "0",
                    "X-Rate-Limit-Reset": "2020-01-02T00:00:00.000Z",
                },
            )

        if utcnow.date() == datetime.date(2020, 1, 2):
            return Response(
                json.dumps({}),
                status=200,
                headers={
                    "X-Rate-Limit-Action": "retrieve",
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


def test_scan(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/api/v1/scan/",
        method="POST",
    ).respond_with_json(
        {
            "uuid": "dummy",
        }
    )

    got = client.scan(
        "http://example.com",
        visibility="public",
    )
    assert got["uuid"] == "dummy"


def test_bulk_scan(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/api/v1/scan/",
        method="POST",
    ).respond_with_json(
        {
            "uuid": "dummy",
        }
    )

    got = client.bulk_scan(
        [
            "http://example.com",
            "http://example.org",
        ],
        visibility="public",
    )
    assert len(got) == 2

    responses = [r for _, r in got]
    for r in responses:
        assert isinstance(r, dict)
        assert r["uuid"] == "dummy"


@pytest.mark.timeout(10)
def test_wait_for_result(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="HEAD",
    ).respond_with_response(Response("", status=200))
    assert client.wait_for_result("dummy", initial_wait=0.0) is None  # type: ignore


@pytest.mark.timeout(10)
def test_scan_and_get_result(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/api/v1/scan/",
        method="POST",
    ).respond_with_json(
        {
            "uuid": "dummy",
        }
    )
    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="HEAD",
    ).respond_with_response(Response("", status=200))
    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="GET",
    ).respond_with_json(
        {
            "task": {"uuid": "dummy"},
        }
    )

    got = client.scan_and_get_result(
        "http://example.com", visibility="public", initial_wait=0.0
    )
    assert got["task"]["uuid"] == "dummy"


@pytest.mark.timeout(10)
def test_bulk_scan_and_get_results(client: Client, httpserver: HTTPServer):
    httpserver.expect_request(
        "/api/v1/scan/",
        method="POST",
    ).respond_with_json(
        {
            "uuid": "dummy",
        }
    )
    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="HEAD",
    ).respond_with_response(Response("", status=200))
    httpserver.expect_request(
        "/api/v1/result/dummy/",
        method="GET",
    ).respond_with_json(
        {
            "task": {"uuid": "dummy"},
        }
    )

    got = client.bulk_scan_and_get_results(
        [
            "http://example.com",
            "http://example.org",
        ],
        visibility="public",
        initial_wait=0.0,
    )
    assert len(got) == 2
    results = [r for _, r in got]
    for r in results:
        assert isinstance(r, dict)
        assert r["task"]["uuid"] == "dummy"
