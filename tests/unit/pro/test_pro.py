from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_user(pro: Pro, httpserver: HTTPServer):
    data = {
        "username": "example_user",
        "email": "user@example.com",
        "createdAt": "2023-01-15T10:30:00.000Z",
        "team": {
            "_id": "team-id-12345",
            "name": "Example Team",
            "slug": "example-team",
        },
        "limits": {
            "private": {
                "day": {"limit": 20000, "used": 150, "remaining": 19850, "percent": 1},
                "hour": {"limit": 2000, "used": 25, "remaining": 1975, "percent": 1},
                "minute": {"limit": 120, "used": 2, "remaining": 118, "percent": 2},
            },
            "public": {
                "day": {"limit": 50000, "used": 500, "remaining": 49500, "percent": 1},
                "hour": {"limit": 5000, "used": 50, "remaining": 4950, "percent": 1},
                "minute": {"limit": 120, "used": 5, "remaining": 115, "percent": 4},
            },
        },
        "products": ["pro", "livescan"],
        "features": ["country-select", "livescan/tier/base", "api/extended-quotas"],
    }
    httpserver.expect_request(
        "/api/v1/pro/username",
        method="GET",
    ).respond_with_json(data)

    got = pro.get_user()
    assert got == data


def test_lookup_malicious_observable(pro: Pro, httpserver: HTTPServer):
    type_ = "url"
    value = "https://example.com"
    data = {
        "type": type_,
        "value": value,
        "count": 5,
        "lastSeen": "2024-06-01T12:00:00.000Z",
        "firstSeen": "2024-01-01T08:00:00.000Z",
    }
    httpserver.expect_request(
        # pytest-httpserver (werkzeug) normalizes URL path so no need to quote_plus it in the test
        f"/api/v1/malicious/{type_}/{value}",
        method="GET",
    ).respond_with_json(data)

    got = pro.lookup_malicious_observable(type_, value)  # type: ignore[arg-type]
    assert got == data
