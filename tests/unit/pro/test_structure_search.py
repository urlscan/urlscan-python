from pytest_httpserver import HTTPServer

from urlscan import Pro


def test_structure_search(pro: Pro, httpserver: HTTPServer):
    scan_id = "test-scan-id"
    q = "foo"

    # set first request & response
    httpserver.expect_request(
        f"/api/v1/pro/result/{scan_id}/similar/",
        method="GET",
        query_string={"q": q, "size": "100"},
    ).respond_with_json(
        {"results": [{"sort": [1, "dummy"]}], "has_more": False, "total": 1}
    )

    got = list(pro.structure_search(scan_id, q=q))
    # it should return 1 result
    assert len(got) == 1
    # but it should make 1 request
    assert len(httpserver.log) == 1


def test_structure_search_with_multiple_iterations(pro: Pro, httpserver: HTTPServer):
    scan_id = "test-scan-id"
    q = "foo"

    # set first request & response
    httpserver.expect_request(
        f"/api/v1/pro/result/{scan_id}/similar/",
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
        f"/api/v1/pro/result/{scan_id}/similar/",
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
        f"/api/v1/pro/result/{scan_id}/similar/",
        method="GET",
        query_string={"q": q, "size": "10000", "search_after": "10001,dummy"},
    ).respond_with_json(
        {
            "results": [],
            "has_more": True,
            "total": 10000,
        }
    )

    got = list(pro.structure_search(scan_id, q=q, size=10000))
    assert len(got) == 10001
    assert len(httpserver.log) == 2


def test_structure_search_with_limit(pro: Pro, httpserver: HTTPServer):
    scan_id = "test-scan-id"
    q = "foo"

    httpserver.expect_request(
        f"/api/v1/pro/result/{scan_id}/similar/",
        method="GET",
        query_string={"q": q, "size": "100"},
    ).respond_with_json(
        {
            "results": [{"sort": [i, "dummy"]} for i in range(1, 100)],
            "has_more": True,
            "total": 10000,
        }
    )

    got = list(pro.structure_search(scan_id, q=q, limit=10))
    assert len(got) == 10
    assert len(httpserver.log) == 1
