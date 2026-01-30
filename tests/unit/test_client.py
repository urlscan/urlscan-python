import datetime
import json
import tempfile

import pytest
from freezegun.api import FrozenDateTimeFactory
from pytest_httpserver import HTTPServer
from werkzeug import Request, Response

from urlscan import Client
from urlscan.error import APIError, RateLimitError, RateLimitRemainingError


def test_get(client: Client, httpserver: HTTPServer):
    data = {"foo": "bar"}
    httpserver.expect_request("/dummy").respond_with_json(data)

    got = client._get("/dummy")
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

    got = client._post("/dummy")
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

    got = client._get("/dummy")
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


def test_get_available_countries(client: Client, httpserver: HTTPServer):
    data = {
        "countries": [
            "de",
            "us",
            "jp",
        ]
    }
    httpserver.expect_request(
        "/api/v1/availableCountries",
        method="GET",
    ).respond_with_json(data)

    got = client.get_available_countries()
    assert got == data


def test_get_user_agents(client: Client, httpserver: HTTPServer):
    data = {
        "userAgents": [
            {
                "group": "Chrome",
                "useragents": [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
                ],
            },
            {
                "group": "iOS",
                "useragents": [
                    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
                ],
            },
        ]
    }
    httpserver.expect_request(
        "/api/v1/userAgents",
        method="GET",
    ).respond_with_json(data)

    got = client.get_user_agents()
    assert got == data


def test_get_quotas(client: Client, httpserver: HTTPServer):
    data = {
        "scope": "team",
        "limits": {
            "private": {
                "day": {"limit": 20000, "used": 0, "remaining": 20000, "percent": 0},
            },
            "search": {
                "day": {
                    "limit": 500000,
                    "used": 1389,
                    "remaining": 498611,
                    "reset": "2023-09-30T00:00:00.000Z",
                    "percent": 0,
                },
            },
            "unlisted": {
                "day": {"limit": 40000, "used": 0, "remaining": 40000, "percent": 0},
            },
            "livescan": {
                "day": {"limit": 10000, "used": 0, "remaining": 10000, "percent": 0},
            },
        },
    }
    httpserver.expect_request(
        "/api/v1/quotas",
        method="GET",
    ).respond_with_json(data)

    got = client.get_quotas()
    assert got == data


def test_error_1(client: Client, httpserver: HTTPServer):
    # basic error
    httpserver.expect_request(
        "/error",
        method="GET",
    ).respond_with_json(
        {
            "message": "DNS Error - Could not resolve domain",
            "description": "The domain foo.bar could not be resolved to a valid IPv4/IPv6 address. We won't try to load it in the browser.",
            "status": 400,
            "errors": [
                {
                    "title": "DNS Error - Could not resolve domain",
                    "detail": "The domain foo.bar could not be resolved to a valid IPv4/IPv6 address. We won't try to load it in the browser.",
                    "status": 400,
                }
            ],
        },
        status=400,
    )
    with pytest.raises(APIError) as exc_info:
        client.get_json("/error")

    exc = exc_info.value
    assert exc.status == 400
    assert (
        exc.description
        == "The domain foo.bar could not be resolved to a valid IPv4/IPv6 address. We won't try to load it in the browser."
    )
    assert len(exc.errors or []) == 1

    error_item = (exc.errors or [])[0]
    assert error_item.title == "DNS Error - Could not resolve domain"
    assert error_item.status == 400
    assert (
        error_item.detail
        == "The domain foo.bar could not be resolved to a valid IPv4/IPv6 address. We won't try to load it in the browser."
    )


def test_error_2(client: Client, httpserver: HTTPServer):
    # validation error
    httpserver.expect_request(
        "/error",
        method="GET",
    ).respond_with_json(
        {
            "code": "validationerror",
            "type": "body",
            "message": 'ValidationError: "url" is required. "foo" is not allowed',
            "errors": [
                {
                    "code": "validationerror",
                    "title": "Field Validation Error",
                    "description": 'ValidationError: "url" is required. "foo" is not allowed',
                    "status": 400,
                }
            ],
        },
        status=400,
    )
    with pytest.raises(APIError) as exc_info:
        client.get_json("/error")

    exc = exc_info.value
    assert exc.status == 400
    assert exc.code == "validationerror"
    assert exc.type == "body"
    assert exc.message == 'ValidationError: "url" is required. "foo" is not allowed'
    assert len(exc.errors or []) == 1
    error_item = (exc.errors or [])[0]
    assert error_item.code == "validationerror"
    assert error_item.title == "Field Validation Error"
    assert (
        error_item.description
        == 'ValidationError: "url" is required. "foo" is not allowed'
    )


def test_error_3(client: Client, httpserver: HTTPServer):
    # basic error without description
    httpserver.expect_request(
        "/error",
        method="GET",
    ).respond_with_json(
        {
            "message": 'No API key supplied. Please supply a valid API key in the "api-key" HTTP header.',
            "status": 401,
            "errors": [
                {
                    "title": 'No API key supplied. Please supply a valid API key in the "api-key" HTTP header.',
                    "detail": 'No API key supplied. Please supply a valid API key in the "api-key" HTTP header.',
                    "status": 401,
                }
            ],
        },
        status=401,
    )
    with pytest.raises(APIError) as exc_info:
        client.get_json("/error")

    exc = exc_info.value
    assert exc.status == 401
    assert (
        exc.message
        == 'No API key supplied. Please supply a valid API key in the "api-key" HTTP header.'
    )
    assert exc.description is None
    assert exc.code is None
    assert exc.type is None
    assert exc.errors is not None
