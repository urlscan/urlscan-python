from typing import Any

from pytest_httpserver import HTTPServer
from pytest_httpserver.httpserver import Response

from urlscan.pro import Pro


def test_get_list(pro: Pro, httpserver: HTTPServer):
    data: dict[str, Any] = {"files": []}
    httpserver.expect_request(
        "/api/v1/datadump/list/days/api/20260101/"
    ).respond_with_json(data)

    got = pro.datadump.get_list("days/api/20260101/")
    assert got == data


def test_download_file(pro: Pro, httpserver: HTTPServer, tmp_path):
    httpserver.expect_request(
        "/api/v1/datadump/link/days/api/20260101/testfile.gz"
    ).respond_with_response(
        Response(
            status=302,
            headers={"Location": httpserver.url_for("/dummy")},
        )
    )
    content = b"test content"
    httpserver.expect_request(
        "/dummy",
    ).respond_with_data(content, content_type="application/gzip")

    file_path = tmp_path / "testfile.gz"
    with open(file_path, "wb") as file:
        pro.datadump.download_file(
            "days/api/20260101/testfile.gz",
            file=file,
        )

    with open(file_path, "rb") as file:
        got = file.read()

    assert got == content
