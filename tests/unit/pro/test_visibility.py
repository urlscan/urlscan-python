from typing import Any

import pytest
from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_update(pro: Pro, httpserver: HTTPServer):
    expected: dict[str, Any] = {
        "uuid": "dummy",
        "message": "Visibility updated",
        "visibility": "public",
    }
    httpserver.expect_request(
        "/api/v1/result/dummy/visibility/", method="PUT", json={"visibility": "public"}
    ).respond_with_json(expected)

    got = pro.visibility.update("dummy", "public")
    assert got == expected


def test_update_with_invalid_visibility(pro: Pro):
    with pytest.raises(ValueError):
        pro.visibility.update("dummy", "invalid")  # type: ignore


def test_reset(pro: Pro, httpserver: HTTPServer):
    expected: dict[str, Any] = {
        "uuid": "dummy",
        "message": "Visibility reset to public",
    }
    httpserver.expect_request(
        "/api/v1/result/dummy/visibility/", method="DELETE"
    ).respond_with_json(expected)

    got = pro.visibility.reset("dummy")
    assert got == expected
