from typing import Any

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_list(pro: Pro, httpserver: HTTPServer):
    data: dict[str, Any] = {
        "searches": [
            {
                "_id": "dummy-id",
                "datasource": "scans",
                "query": "page.domain:urlscan.io",
                "name": "Testsearch",
                "description": "urlscan documentation example saved search.",
                "longDescription": "Example saved search created from urlscan documentation.",
                "tlp": "red",
                "userTags": ["private.privatetag"],
                "permissions": ["team:read", "team:write"],
            }
        ]
    }
    httpserver.expect_request("/api/v1/user/searches/").respond_with_json(data)

    got = pro.saved_search.get_list()
    assert got == data


def test_create_minimal(pro: Pro, httpserver: HTTPServer):
    data = {
        "search": {
            "_id": "dummy-id",
            "datasource": "scans",
            "query": "page.domain:example.com",
            "name": "Example Search",
        }
    }
    httpserver.expect_request(
        "/api/v1/user/searches/",
        method="POST",
        json={
            "search": {
                "datasource": "scans",
                "query": "page.domain:example.com",
                "name": "Example Search",
            },
        },
    ).respond_with_json(data)

    got = pro.saved_search.create(
        datasource="scans",
        query="page.domain:example.com",
        name="Example Search",
    )
    assert got == data


def test_create_with_all_params(pro: Pro, httpserver: HTTPServer):
    data = {
        "search": {
            "_id": "dummy-id",
            "datasource": "hostnames",
            "query": "hostname:*.example.com",
            "name": "Hostname Search",
            "description": "Short description",
            "longDescription": "Detailed description of the search",
            "tlp": "amber",
            "userTags": ["tag1", "tag2"],
            "permissions": ["public:read", "team:write"],
        }
    }
    httpserver.expect_request(
        "/api/v1/user/searches/",
        method="POST",
        json={
            "search": {
                "datasource": "hostnames",
                "query": "hostname:*.example.com",
                "name": "Hostname Search",
                "description": "Short description",
                "longDescription": "Detailed description of the search",
                "tlp": "amber",
                "userTags": ["tag1", "tag2"],
                "permissions": ["public:read", "team:write"],
            }
        },
    ).respond_with_json(data)

    got = pro.saved_search.create(
        datasource="hostnames",
        query="hostname:*.example.com",
        name="Hostname Search",
        description="Short description",
        long_description="Detailed description of the search",
        tlp="amber",
        user_tags=["tag1", "tag2"],
        permissions=["public:read", "team:write"],
    )
    assert got == data


def test_update_minimal(pro: Pro, httpserver: HTTPServer):
    search_id = "test-search-id"
    data = {
        "search": {
            "_id": search_id,
            "datasource": "scans",
            "query": "page.domain:updated.com",
            "name": "Updated Search",
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/searches/{search_id}/",
        method="PUT",
        json={
            "search": {
                "datasource": "scans",
                "query": "page.domain:updated.com",
                "name": "Updated Search",
            }
        },
    ).respond_with_json(data)

    got = pro.saved_search.update(
        search_id=search_id,
        datasource="scans",
        query="page.domain:updated.com",
        name="Updated Search",
    )
    assert got == data


def test_update_with_all_params(pro: Pro, httpserver: HTTPServer):
    search_id = "test-search-id"
    data = {
        "search": {
            "_id": search_id,
            "datasource": "hostnames",
            "query": "hostname:*.updated.com",
            "name": "Updated Hostname Search",
            "description": "Updated short description",
            "longDescription": "Updated detailed description",
            "tlp": "green",
            "userTags": ["updated-tag"],
            "permissions": ["team:read"],
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/searches/{search_id}/",
        method="PUT",
        json={
            "search": {
                "datasource": "hostnames",
                "query": "hostname:*.updated.com",
                "name": "Updated Hostname Search",
                "description": "Updated short description",
                "longDescription": "Updated detailed description",
                "tlp": "green",
                "userTags": ["updated-tag"],
                "permissions": ["team:read"],
            }
        },
    ).respond_with_json(data)

    got = pro.saved_search.update(
        search_id=search_id,
        datasource="hostnames",
        query="hostname:*.updated.com",
        name="Updated Hostname Search",
        description="Updated short description",
        long_description="Updated detailed description",
        tlp="green",
        user_tags=["updated-tag"],
        permissions=["team:read"],
    )
    assert got == data


def test_remove(pro: Pro, httpserver: HTTPServer):
    search_id = "test-search-id"
    data: dict[str, Any] = {}
    httpserver.expect_request(
        f"/api/v1/user/searches/{search_id}/",
        method="DELETE",
    ).respond_with_json(data)

    got = pro.saved_search.remove(search_id=search_id)
    assert got == data


def test_get_results(pro: Pro, httpserver: HTTPServer):
    search_id = "test-search-id"
    data: dict[str, Any] = {
        "results": [
            {
                "task": {
                    "visibility": "public",
                    "method": "automatic",
                    "time": "2023-09-29T03:07:48.446Z",
                    "source": "api",
                    "url": "https://urlscan.io",
                },
                "page": {
                    "url": "https://urlscan.io/",
                    "domain": "urlscan.io",
                    "ip": "104.22.12.171",
                    "status": "200",
                },
                "_id": "dummy-id",
                "result": "https://urlscan.io/api/v1/result/dummy-id/",
                "screenshot": "https://urlscan.io/screenshots/dummy-id.png",
            }
        ],
        "total": 1,
        "took": 15,
        "has_more": False,
    }
    httpserver.expect_request(
        f"/api/v1/user/searches/{search_id}/results/"
    ).respond_with_json(data)

    got = pro.saved_search.get_results(search_id=search_id)
    assert got == data
