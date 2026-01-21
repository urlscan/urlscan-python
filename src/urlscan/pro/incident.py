"""Incident management API client module."""

from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import (
    IncidentVisibilityType,
    ScanIntervalModeType,
    WatchedAttributeType,
)


class Incident(BaseClient):
    """Incident API client."""

    def create(
        self,
        *,
        observable: str,
        visibility: IncidentVisibilityType,
        channels: list[str],
        scan_interval: int | None = None,
        scan_interval_mode: ScanIntervalModeType | None = None,
        watched_attributes: list[WatchedAttributeType] | None = None,
        user_agents: list[str] | None = None,
        user_agents_per_interval: int | None = None,
        countries: list[str] | None = None,
        countries_per_interval: int | None = None,
        stop_delay_suspended: int | None = None,
        stop_delay_inactive: int | None = None,
        stop_delay_malicious: int | None = None,
        scan_interval_after_suspended: int | None = None,
        scan_interval_after_malicious: int | None = None,
        incident_profile: str | None = None,
        expire_after: int | None = None,
    ) -> dict:
        """Create an incident with specific options.

        Args:
            observable (str): Hostname, domain, IP, or URL to observe.
            visibility (IncidentVisibilityType): Scan visibility ("unlisted" or "private").
            channels (list[str]): Channels subscribed to this incident.
            scan_interval (int | None, optional): Interval (seconds) between triggering full website scans. Defaults to None.
            scan_interval_mode (ScanIntervalModeType | None, optional): If this is set to manual then scan_interval_after_suspended and scan_interval_after_malicious will not have an effect ("manual" or "automatic"). Defaults to None.
            watched_attributes (list[WatchedAttributeType] | None, optional): Determine which items will be monitored for (detections, tls, dns, labels, page, meta, ip). Defaults to None.
            user_agents (list[str] | None, optional): Browser User-Agents to use during scanning. Defaults to None.
            user_agents_per_interval (int | None, optional): How many userAgents to use per scanInterval. Defaults to None.
            countries (list[str] | None, optional): List of countries to scan from as ISO-3166-1 country codes. Defaults to None.
            countries_per_interval (int | None, optional): How many countries to use per scan interval. Defaults to None.
            stop_delay_suspended (int | None, optional): When to automatically close the incident after the observable was suspended. Defaults to None.
            stop_delay_inactive (int | None, optional): When to automatically close the incident after the observable became inactive. Defaults to None.
            stop_delay_malicious (int | None, optional): When to automatically close the incident after the observable became malicious. Defaults to None.
            scan_interval_after_suspended (int | None, optional): How to change the scan interval after the observable was suspended. Defaults to None.
            scan_interval_after_malicious (int | None, optional): How to change the scan interval after the observable became malicious. Defaults to None.
            incident_profile (str | None, optional): ID of the incident profile to use when creating this incident. Defaults to None.
            expire_after (int | None, optional): Seconds until the incident will automatically be closed. Defaults to None.

        Returns:
            dict: Incident body.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/createincident

        """
        incident: dict[str, Any] = _compact(
            {
                "observable": observable,
                "visibility": visibility,
                "channels": channels,
                "scanInterval": scan_interval,
                "scanIntervalMode": scan_interval_mode,
                "watchedAttributes": watched_attributes,
                "userAgents": user_agents,
                "userAgentsPerInterval": user_agents_per_interval,
                "countries": countries,
                "countriesPerInterval": countries_per_interval,
                "stopDelaySuspended": stop_delay_suspended,
                "stopDelayInactive": stop_delay_inactive,
                "stopDelayMalicious": stop_delay_malicious,
                "scanIntervalAfterSuspended": scan_interval_after_suspended,
                "scanIntervalAfterMalicious": scan_interval_after_malicious,
                "incidentProfile": incident_profile,
                "expireAfter": expire_after,
            }
        )
        data = {"incident": incident}

        res = self._post("/api/v1/user/incidents", json=data)
        return self._response_to_json(res)

    def get(self, incident_id: str) -> dict:
        """Get details for a specific incident.

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Incident body.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/getincident

        """
        return super().get_json(f"/api/v1/user/incidents/{incident_id}")

    def update(
        self,
        incident_id: str,
        *,
        observable: str,
        visibility: IncidentVisibilityType,
        channels: list[str],
        scan_interval: int | None = None,
        scan_interval_mode: ScanIntervalModeType | None = None,
        watched_attributes: list[WatchedAttributeType] | None = None,
        user_agents: list[str] | None = None,
        user_agents_per_interval: int | None = None,
        countries: list[str] | None = None,
        countries_per_interval: int | None = None,
        stop_delay_suspended: int | None = None,
        stop_delay_inactive: int | None = None,
        stop_delay_malicious: int | None = None,
        scan_interval_after_suspended: int | None = None,
        scan_interval_after_malicious: int | None = None,
        incident_profile: str | None = None,
        expire_after: int | None = None,
    ) -> dict:
        """Update specific runtime options of the incident.

        Args:
            incident_id (str): ID of incident.
            observable (str): Hostname, domain, IP, or URL to observe.
            visibility (IncidentVisibilityType): Scan visibility ("unlisted" or "private").
            channels (list[str]): Channels subscribed to this incident.
            scan_interval (int | None, optional): Interval (seconds) between triggering full website scans. Defaults to None.
            scan_interval_mode (ScanIntervalModeType | None, optional): If this is set to manual then scan_interval_after_suspended and scan_interval_after_malicious will not have an effect ("manual" or "automatic"). Defaults to None.
            watched_attributes (list[WatchedAttributeType] | None, optional): Determine which items will be monitored for (detections, tls, dns, labels, page, meta, ip). Defaults to None.
            user_agents (list[str] | None, optional): Browser User-Agents to use during scanning. Defaults to None.
            user_agents_per_interval (int | None, optional): How many userAgents to use per scanInterval. Defaults to None.
            countries (list[str] | None, optional): List of countries to scan from as ISO-3166-1 country codes. Defaults to None.
            countries_per_interval (int | None, optional): How many countries to use per scan interval. Defaults to None.
            stop_delay_suspended (int | None, optional): When to automatically close the incident after the observable was suspended. Defaults to None.
            stop_delay_inactive (int | None, optional): When to automatically close the incident after the observable became inactive. Defaults to None.
            stop_delay_malicious (int | None, optional): When to automatically close the incident after the observable became malicious. Defaults to None.
            scan_interval_after_suspended (int | None, optional): How to change the scan interval after the observable was suspended. Defaults to None.
            scan_interval_after_malicious (int | None, optional): How to change the scan interval after the observable became malicious. Defaults to None.
            incident_profile (str | None, optional): ID of the incident profile to use when creating this incident. Defaults to None.
            expire_after (int | None, optional): Seconds until the incident will automatically be closed. Defaults to None.

        Returns:
            dict: Incident body.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/updateincident

        """
        incident: dict[str, Any] = _compact(
            {
                "observable": observable,
                "visibility": visibility,
                "channels": channels,
                "scanInterval": scan_interval,
                "scanIntervalMode": scan_interval_mode,
                "watchedAttributes": watched_attributes,
                "userAgents": user_agents,
                "userAgentsPerInterval": user_agents_per_interval,
                "countries": countries,
                "countriesPerInterval": countries_per_interval,
                "stopDelaySuspended": stop_delay_suspended,
                "stopDelayInactive": stop_delay_inactive,
                "stopDelayMalicious": stop_delay_malicious,
                "scanIntervalAfterSuspended": scan_interval_after_suspended,
                "scanIntervalAfterMalicious": scan_interval_after_malicious,
                "incidentProfile": incident_profile,
                "expireAfter": expire_after,
            }
        )
        data = {"incident": incident}

        res = self._put(f"/api/v1/user/incidents/{incident_id}", json=data)
        return self._response_to_json(res)

    def close(self, *, incident_id: str) -> dict:
        """Close (stop) the incident.

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Response confirming closure.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/closeincident

        """
        res = self._put(f"/api/v1/user/incidents/{incident_id}/close", json={})
        return self._response_to_json(res)

    def restart(self, incident_id: str) -> dict:
        """Restart a closed incident.

        Automatically extends the incident expireAt. Starts with new incident states.

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Response confirming restart.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/restartincident

        """
        res = self._put(f"/api/v1/user/incidents/{incident_id}/restart", json={})
        return self._response_to_json(res)

    def copy(self, incident_id: str) -> dict:
        """Copy an incident without its history.

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Incident body.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/copyincident

        """
        res = self._post(f"/api/v1/user/incidents/{incident_id}/copy", json={})
        return self._response_to_json(res)

    def fork(self, incident_id: str) -> dict:
        """Copy an incident along with its history (incident states).

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Incident body.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/forkincident

        """
        res = self._post(f"/api/v1/user/incidents/{incident_id}/fork", json={})
        return self._response_to_json(res)

    def get_watchable_attributes(self) -> dict:
        """Get the list of attributes which can be supplied to the watchedAttributes property of the incident.

        Returns:
            dict: List of watchable attributes.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/getwatchableattributes

        """
        return self.get_json("/api/v1/user/watchableAttributes")

    def get_states(self, incident_id: str) -> dict:
        """Retrieve individual incident states of an incident.

        Args:
            incident_id (str): ID of incident.

        Returns:
            dict: Incident states.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/incidents/getincidentstates

        """
        return self.get_json(f"/api/v1/user/incidentstates/{incident_id}/")
