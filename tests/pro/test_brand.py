from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_available(pro: Pro, httpserver: HTTPServer):
    data = {
        "kits": [
            {
                "_id": "brand-id-1",
                "name": "Example Brand",
                "key": "example",
                "vertical": ["financial"],
                "country": ["US"],
                "terms": {
                    "domains": ["example.com", "example.org"],
                    "asns": ["AS12345"],
                },
                "createdAt": "2024-01-01T00:00:00Z",
            },
            {
                "_id": "brand-id-2",
                "name": "Another Brand",
                "key": "another",
                "vertical": ["technology"],
                "country": ["GB", "DE"],
                "terms": {
                    "domains": ["another.com"],
                    "asns": ["AS67890"],
                },
                "createdAt": "2024-02-01T00:00:00Z",
            },
        ]
    }
    httpserver.expect_request(
        "/api/v1/pro/availableBrands",
        method="GET",
    ).respond_with_json(data)

    got = pro.brand.get_available_brands()
    assert got == data


def test_get_brands(pro: Pro, httpserver: HTTPServer):
    data = {
        "responses": [
            {
                "hits": [
                    {
                        "task": {
                            "time": "2024-01-15T10:00:00.000Z",
                            "uuid": "00000000-0000-0000-0000-000000000001",
                        },
                        "brand": [
                            {
                                "country": ["us"],
                                "name": "Example Brand",
                                "vertical": ["financial"],
                                "key": "examplebrand",
                            }
                        ],
                        "_id": "00000000-0000-0000-0000-000000000001",
                        "result": "https://urlscan.io/api/v1/result/00000000-0000-0000-0000-000000000001/",
                    }
                ],
                "total": 1000,
                "brand": {
                    "_id": "000000000000000000000001",
                    "name": "Example Brand",
                    "key": "examplebrand",
                    "vertical": ["financial"],
                    "country": ["us"],
                    "region": ["Americas"],
                    "keywords": [],
                    "terms": {"domains": [], "asns": []},
                    "createdAt": "2024-01-01T00:00:00.000Z",
                    "updatedAt": "2024-01-01T00:00:00.000Z",
                },
            }
        ]
    }
    httpserver.expect_request(
        "/api/v1/pro/brands",
        method="GET",
    ).respond_with_json(data)

    got = pro.brand.get_brands()
    assert got == data
