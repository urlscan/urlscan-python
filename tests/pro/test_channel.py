from typing import Any

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_get_channels(pro: Pro, httpserver: HTTPServer):
    data: dict[str, Any] = {"channels": []}
    httpserver.expect_request("/api/v1/user/channels/").respond_with_json(data)

    got = pro.channel.get_channels()
    assert got == data


def test_create_webhook_channel(pro: Pro, httpserver: HTTPServer):
    data = {
        "channel": {
            "_id": "test-channel-id",
            "type": "webhook",
            "webhookURL": "https://example.com/webhook",
            "name": "Test Webhook Channel",
            "isActive": True,
            "ignoreTime": False,
        }
    }
    httpserver.expect_request(
        "/api/v1/user/channels/",
        method="POST",
    ).respond_with_json(data)

    got = pro.channel.create(
        channel_type="webhook",
        name="Test Webhook Channel",
        webhook_url="https://example.com/webhook",
        is_active=True,
        ignore_time=False,
    )
    assert got == data


def test_create_email_channel(pro: Pro, httpserver: HTTPServer):
    data = {
        "channel": {
            "_id": "test-email-channel-id",
            "type": "email",
            "emailAddresses": ["test@example.com"],
            "frequency": "daily",
            "utcTime": "09:00",
            "name": "Test Email Channel",
            "isActive": True,
            "ignoreTime": False,
        }
    }
    httpserver.expect_request(
        "/api/v1/user/channels/",
        method="POST",
    ).respond_with_json(data)

    got = pro.channel.create(
        channel_type="email",
        name="Test Email Channel",
        email_addresses=["test@example.com"],
        frequency="daily",
        utc_time="09:00",
        is_active=True,
        ignore_time=False,
    )
    assert got == data


def test_get(pro: Pro, httpserver: HTTPServer):
    channel_id = "test-channel-id"
    data = {
        "channel": {
            "_id": channel_id,
            "type": "webhook",
            "webhookURL": "https://example.com/webhook",
            "name": "Test Webhook Channel",
            "isActive": True,
        }
    }
    httpserver.expect_request(f"/api/v1/user/channels/{channel_id}/").respond_with_json(
        data
    )

    got = pro.channel.get(channel_id=channel_id)
    assert got == data


def test_update_webhook_channel(pro: Pro, httpserver: HTTPServer):
    channel_id = "test-channel-id"
    data = {
        "channel": {
            "_id": channel_id,
            "type": "webhook",
            "webhookURL": "https://example.com/updated-webhook",
            "name": "Updated Webhook Channel",
            "isActive": False,
            "ignoreTime": True,
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/channels/{channel_id}/",
        method="PUT",
    ).respond_with_json(data)

    got = pro.channel.update(
        channel_id=channel_id,
        channel_type="webhook",
        name="Updated Webhook Channel",
        webhook_url="https://example.com/updated-webhook",
        is_active=False,
        ignore_time=True,
    )
    assert got == data


def test_update_email_channel(pro: Pro, httpserver: HTTPServer):
    channel_id = "test-email-channel-id"
    data = {
        "channel": {
            "_id": channel_id,
            "type": "email",
            "emailAddresses": ["updated@example.com"],
            "frequency": "hourly",
            "name": "Updated Email Channel",
            "isActive": True,
            "weekDays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/channels/{channel_id}/",
        method="PUT",
    ).respond_with_json(data)

    got = pro.channel.update(
        channel_id=channel_id,
        channel_type="email",
        name="Updated Email Channel",
        email_addresses=["updated@example.com"],
        frequency="hourly",
        is_active=True,
        week_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    )
    assert got == data


def test_create_with_permissions(pro: Pro, httpserver: HTTPServer):
    data = {
        "channel": {
            "_id": "test-channel-id",
            "type": "webhook",
            "webhookURL": "https://example.com/webhook",
            "name": "Team Webhook Channel",
            "isActive": True,
            "permissions": ["team:read", "team:write"],
        }
    }
    httpserver.expect_request(
        "/api/v1/user/channels/",
        method="POST",
    ).respond_with_json(data)

    got = pro.channel.create(
        channel_type="webhook",
        name="Team Webhook Channel",
        webhook_url="https://example.com/webhook",
        is_active=True,
        permissions=["team:read", "team:write"],
    )
    assert got == data
