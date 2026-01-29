from pytest_httpserver import HTTPServer

from urlscan import Pro


def test_hostname(pro: Pro, httpserver: HTTPServer):
    hostname = "example.com"

    httpserver.expect_request(
        f"/api/v1/hostname/{hostname}",
        method="GET",
        query_string={"limit": "1000"},
    ).respond_with_json({"results": [{"sub_id": "dummy"}], "pageState": None})

    got = list(pro.hostname(hostname))
    assert len(got) == 1
    assert len(httpserver.log) == 1


def test_hostname_with_pagination(pro: Pro, httpserver: HTTPServer):
    hostname = "example.com"

    # first request returns a pageState for pagination
    httpserver.expect_request(
        f"/api/v1/hostname/{hostname}",
        method="GET",
        query_string={"limit": "1"},
    ).respond_with_json({"results": [{"sub_id": "dummy1"}], "pageState": "state1"})

    # second request uses the pageState
    httpserver.expect_request(
        f"/api/v1/hostname/{hostname}",
        method="GET",
        query_string={"limit": "1", "pageState": "state1"},
    ).respond_with_json({"results": [{"sub_id": "dummy2"}], "pageState": None})

    iterator = pro.hostname(hostname)
    iterator._size = 1

    got = list(iterator)
    assert len(got) == 2
    assert len(httpserver.log) == 2


def test_hostname_with_limit(pro: Pro, httpserver: HTTPServer):
    hostname = "example.com"

    httpserver.expect_request(
        f"/api/v1/hostname/{hostname}",
        method="GET",
        query_string={"limit": "1000"},
    ).respond_with_json(
        {"results": [{"sub_id": f"dummy{i}"} for i in range(10)], "pageState": "state1"}
    )

    iterator = pro.hostname(hostname, limit=3)

    got = list(iterator)
    assert len(got) == 3
    # only one request made because limit is reached before pagination
    assert len(httpserver.log) == 1


def test_hostname_empty_results(pro: Pro, httpserver: HTTPServer):
    hostname = "example.com"

    httpserver.expect_request(
        f"/api/v1/hostname/{hostname}",
        method="GET",
        query_string={"limit": "1000"},
    ).respond_with_json({"results": [], "pageState": None})

    got = list(pro.hostname(hostname))
    assert len(got) == 0
    assert len(httpserver.log) == 1
