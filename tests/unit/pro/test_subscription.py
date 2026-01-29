from typing import Any

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_subscriptions(pro: Pro, httpserver: HTTPServer):
    data: dict[str, Any] = {"subscriptions": []}
    httpserver.expect_request("/api/v1/user/subscriptions/").respond_with_json(data)

    got = pro.subscription.get_subscriptions()
    assert got == data


def test_create(pro: Pro, httpserver: HTTPServer):
    data = {
        "subscription": {
            "_id": "test-subscription-id",
            "searchIds": ["test-search-id"],
            "frequency": "daily",
            "emailAddresses": ["test@example.com"],
            "name": "Test Subscription",
            "description": "Test description",
            "isActive": True,
            "ignoreTime": False,
        }
    }
    httpserver.expect_request(
        "/api/v1/user/subscriptions/",
        method="POST",
    ).respond_with_json(data)

    got = pro.subscription.create(
        search_ids=["test-search-id"],
        frequency="daily",
        email_addresses=["test@example.com"],
        name="Test Subscription",
        description="Test description",
        is_active=True,
        ignore_time=False,
    )
    assert got == data


def test_update(pro: Pro, httpserver: HTTPServer):
    subscription_id = "test-subscription-id"
    data = {
        "subscription": {
            "searchIds": ["test-search-id"],
            "frequency": "hourly",
            "emailAddresses": ["updated@example.com"],
            "name": "Updated Subscription",
            "description": "Updated description",
            "isActive": False,
            "ignoreTime": True,
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/subscriptions/{subscription_id}/",
        method="PUT",
    ).respond_with_json(data)

    got = pro.subscription.update(
        subscription_id=subscription_id,
        search_ids=["test-search-id"],
        frequency="hourly",
        email_addresses=["updated@example.com"],
        name="Updated Subscription",
        description="Updated description",
        is_active=False,
        ignore_time=True,
    )
    assert got == data


def test_delete_subscription(pro: Pro, httpserver: HTTPServer):
    subscription_id = "test-subscription-id"
    data: dict[str, Any] = {}
    httpserver.expect_request(
        f"/api/v1/user/subscriptions/{subscription_id}/",
        method="DELETE",
    ).respond_with_json(data)

    got = pro.subscription.delete_subscription(subscription_id=subscription_id)
    assert got == data


def test_get_results(pro: Pro, httpserver: HTTPServer):
    subscription_id = "test-subscription-id"
    datasource = "scans"
    data: dict[str, Any] = {"results": []}
    httpserver.expect_request(
        f"/api/v1/user/subscriptions/{subscription_id}/results/{datasource}/"
    ).respond_with_json(data)

    got = pro.subscription.get_results(
        subscription_id=subscription_id, datasource=datasource
    )
    assert got == data
