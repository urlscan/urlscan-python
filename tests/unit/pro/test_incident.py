from typing import Any

from pytest_httpserver import HTTPServer

from urlscan.pro import Pro


def test_create(pro: Pro, httpserver: HTTPServer):
    data = {
        "incident": {
            "_id": "test-incident-id",
            "observable": "example.com",
            "visibility": "private",
            "channels": ["test-channel-id"],
            "scanInterval": 3600,
            "scanIntervalMode": "automatic",
            "watchedAttributes": ["detections", "tls"],
            "state": "active",
        }
    }
    httpserver.expect_request(
        "/api/v1/user/incidents",
        method="POST",
    ).respond_with_json(data)

    got = pro.incident.create(
        observable="example.com",
        visibility="private",
        channels=["test-channel-id"],
        scan_interval=3600,
        scan_interval_mode="automatic",
        watched_attributes=["detections", "tls"],
    )
    assert got == data


def test_get_incident(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data = {
        "incident": {
            "_id": incident_id,
            "observable": "example.com",
            "visibility": "private",
            "channels": ["test-channel-id"],
            "state": "active",
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}",
        method="GET",
    ).respond_with_json(data)

    got = pro.incident.get(incident_id=incident_id)
    assert got == data


def test_update(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data = {
        "incident": {
            "_id": incident_id,
            "observable": "updated.com",
            "visibility": "unlisted",
            "channels": ["updated-channel-id"],
            "scanInterval": 7200,
            "state": "active",
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}",
        method="PUT",
    ).respond_with_json(data)

    got = pro.incident.update(
        incident_id=incident_id,
        observable="updated.com",
        visibility="unlisted",
        channels=["updated-channel-id"],
        scan_interval=7200,
    )
    assert got == data


def test_close(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data: dict[str, Any] = {"message": "Incident closed"}
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}/close",
        method="PUT",
    ).respond_with_json(data)

    got = pro.incident.close(incident_id=incident_id)
    assert got == data


def test_restart(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data: dict[str, Any] = {"message": "Incident restarted"}
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}/restart",
        method="PUT",
    ).respond_with_json(data)

    got = pro.incident.restart(incident_id=incident_id)
    assert got == data


def test_copy(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data = {
        "incident": {
            "_id": "new-incident-id",
            "observable": "example.com",
            "visibility": "private",
            "channels": ["test-channel-id"],
            "state": "active",
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}/copy",
        method="POST",
    ).respond_with_json(data)

    got = pro.incident.copy(incident_id=incident_id)
    assert got == data


def test_fork(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data = {
        "incident": {
            "_id": "forked-incident-id",
            "observable": "example.com",
            "visibility": "private",
            "channels": ["test-channel-id"],
            "state": "active",
        }
    }
    httpserver.expect_request(
        f"/api/v1/user/incidents/{incident_id}/fork",
        method="POST",
    ).respond_with_json(data)

    got = pro.incident.fork(incident_id=incident_id)
    assert got == data


def test_get_watchable_attributes(pro: Pro, httpserver: HTTPServer):
    data = {"attributes": ["detections", "tls", "dns", "labels", "page", "meta", "ip"]}
    httpserver.expect_request(
        "/api/v1/user/watchableAttributes",
        method="GET",
    ).respond_with_json(data)

    got = pro.incident.get_watchable_attributes()
    assert got == data


def test_get_incident_states(pro: Pro, httpserver: HTTPServer):
    incident_id = "test-incident-id"
    data = {
        "incidentstates": [
            {
                "_id": "state-1",
                "incident": incident_id,
                "state": {"status": "active"},
                "timeStart": "2024-01-01T00:00:00Z",
                "timeEnd": "2024-01-01T01:00:00Z",
            }
        ]
    }
    httpserver.expect_request(
        f"/api/v1/user/incidentstates/{incident_id}/",
        method="GET",
    ).respond_with_json(data)

    got = pro.incident.get_states(incident_id=incident_id)
    assert got == data
