from typing import Any

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_scanners(pro: Pro, httpserver: HTTPServer):
    data: dict[str, Any] = {"scanners": []}
    httpserver.expect_request("/api/v1/livescan/scanners/").respond_with_json(data)

    got = pro.livescan.get_scanners()
    assert got == data


def test_task(pro: Pro, httpserver: HTTPServer):
    data = {"uuid": "dummy-uuid"}
    httpserver.expect_request(
        "/api/v1/livescan/de01/task/",
        method="POST",
    ).respond_with_json(data)

    got = pro.livescan.task(scanner_id="de01", url="http://example.com")
    assert got == data


def test_scan(pro: Pro, httpserver: HTTPServer):
    data = {"uuid": "dummy-uuid"}
    httpserver.expect_request(
        "/api/v1/livescan/de01/scan/",
        method="POST",
    ).respond_with_json(data)

    got = pro.livescan.scan(scanner_id="de01", url="http://example.com")
    assert got == data


def test_purge(pro: Pro, httpserver: HTTPServer):
    data = {"status": "purged"}
    httpserver.expect_request(
        "/api/v1/livescan/de01/dummy-uuid/",
        method="DELETE",
    ).respond_with_json(data)

    got = pro.livescan.purge(scanner_id="de01", scan_id="dummy-uuid")
    assert got == data
