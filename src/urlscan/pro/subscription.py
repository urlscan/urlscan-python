"""Subscription management API client module."""

from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import (
    FrequencyType,
    IncidentCreationModeType,
    IncidentVisibilityType,
    IncidentWatchKeyType,
    SubscriptionPermissionType,
    WeekDaysType,
)


class Subscription(BaseClient):
    """Subscription API client."""

    def get_subscriptions(self) -> dict:
        """Get a list of Subscriptions for the current user.

        Returns:
            dict: List of subscriptions.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/subscriptions/subscriptions

        """
        return self.get_json("/api/v1/user/subscriptions/")

    def create(
        self,
        *,
        search_ids: list[str],
        frequency: FrequencyType,
        email_addresses: list[str],
        name: str,
        is_active: bool,
        ignore_time: bool,
        description: str | None = None,
        week_days: list[WeekDaysType] | None = None,
        permissions: list[SubscriptionPermissionType] | None = None,
        channel_ids: list[str] | None = None,
        incident_channel_ids: list[str] | None = None,
        incident_profile_id: str | None = None,
        incident_visibility: IncidentVisibilityType | None = None,
        incident_creation_mode: IncidentCreationModeType | None = None,
        incident_watch_keys: IncidentWatchKeyType | None = None,
    ) -> dict:
        """Create a new subscription.

        Args:
            search_ids (list[str]): Array of search IDs associated with this subscription.
            frequency (FrequencyType): Frequency of notifications ("live", "hourly", or "daily").
            email_addresses (list[str]): Email addresses receiving the notifications.
            name (str): Name of the subscription.
            is_active (bool): Whether the subscription is active.
            ignore_time (bool): Whether to ignore time constraints.
            description (str | None, optional): Description of the subscription. Defaults to None.
            week_days (list[WeekDaysType] | None, optional): Days of the week alerts will be generated (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). Defaults to None.
            permissions (list[SubscriptionPermissionType] | None, optional): Permissions associated with this subscription (team:read, team:write). Defaults to None.
            channel_ids (list[str] | None, optional): Array of channel IDs associated with this subscription. Defaults to None.
            incident_channel_ids (list[str] | None, optional): Array of incident channel IDs associated with this subscription. Defaults to None.
            incident_profile_id (str | None, optional): Incident Profile ID associated with this subscription. Defaults to None.
            incident_visibility (IncidentVisibilityType | None, optional): Incident visibility for this subscription ("unlisted" or "private"). Defaults to None.
            incident_creation_mode (IncidentCreationModeType | None, optional): Incident creation rule for this subscription ("none", "default", "always", or "ignore-if-exists"). Defaults to None.
            incident_watch_keys (IncidentWatchKeyType | None, optional): Source/key to watch in the incident (scans/page.url, scans/page.domain, scans/page.ip, scans/page.apexDomain, hostnames/hostname, hostnames/ip, hostnames/domain). Defaults to None.

        Returns:
            dict: Response containing the created subscription with an '_id' field.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/subscriptions/subscriptionscreate

        """
        subscription: dict[str, Any] = _compact(
            {
                "searchIds": search_ids,
                "frequency": frequency,
                "emailAddresses": email_addresses,
                "name": name,
                "description": description,
                "isActive": is_active,
                "ignoreTime": ignore_time,
                "weekDays": week_days,
                "permissions": permissions,
                "channelIds": channel_ids,
                "incidentChannelIds": incident_channel_ids,
                "incidentProfileId": incident_profile_id,
                "incidentVisibility": incident_visibility,
                "incidentCreationMode": incident_creation_mode,
                "incidentWatchKeys": incident_watch_keys,
            }
        )
        data = {"subscription": subscription}

        res = self._post("/api/v1/user/subscriptions/", json=data)
        return self._response_to_json(res)

    def update(
        self,
        *,
        subscription_id: str,
        search_ids: list[str],
        frequency: FrequencyType,
        email_addresses: list[str],
        name: str,
        is_active: bool,
        ignore_time: bool,
        description: str | None = None,
        week_days: list[WeekDaysType] | None = None,
        permissions: list[SubscriptionPermissionType] | None = None,
        channel_ids: list[str] | None = None,
        incident_channel_ids: list[str] | None = None,
        incident_profile_id: str | None = None,
        incident_visibility: IncidentVisibilityType | None = None,
        incident_creation_mode: IncidentCreationModeType | None = None,
        incident_watch_keys: IncidentWatchKeyType | None = None,
    ) -> dict:
        """Update the settings for a subscription.

        Args:
            subscription_id (str): Subscription ID.
            search_ids (list[str]): Array of search IDs associated with this subscription.
            frequency (FrequencyType): Frequency of notifications ("live", "hourly", or "daily").
            email_addresses (list[str]): Email addresses receiving the notifications.
            name (str): Name of the subscription.
            is_active (bool): Whether the subscription is active.
            ignore_time (bool): Whether to ignore time constraints.
            description (str | None, optional): Description of the subscription. Defaults to None.
            week_days (list[WeekDaysType] | None, optional): Days of the week alerts will be generated (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). Defaults to None.
            permissions (list[SubscriptionPermissionType] | None, optional): Permissions associated with this subscription (team:read, team:write). Defaults to None.
            channel_ids (list[str] | None, optional): Array of channel IDs associated with this subscription. Defaults to None.
            incident_channel_ids (list[str] | None, optional): Array of incident channel IDs associated with this subscription. Defaults to None.
            incident_profile_id (str | None, optional): Incident Profile ID associated with this subscription. Defaults to None.
            incident_visibility (IncidentVisibilityType | None, optional): Incident visibility for this subscription ("unlisted" or "private"). Defaults to None.
            incident_creation_mode (IncidentCreationModeType | None, optional): Incident creation rule for this subscription ("none", "default", "always", or "ignore-if-exists"). Defaults to None.
            incident_watch_keys (IncidentWatchKeyType | None, optional): Source/key to watch in the incident (scans/page.url, scans/page.domain, scans/page.ip, scans/page.apexDomain, hostnames/hostname, hostnames/ip, hostnames/domain). Defaults to None.

        Returns:
            dict: Response containing the updated subscription with an '_id' field.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/subscriptions/subscriptionsget

        """
        subscription: dict[str, Any] = _compact(
            {
                "searchIds": search_ids,
                "frequency": frequency,
                "emailAddresses": email_addresses,
                "name": name,
                "description": description,
                "isActive": is_active,
                "ignoreTime": ignore_time,
                "weekDays": week_days,
                "permissions": permissions,
                "channelIds": channel_ids,
                "incidentChannelIds": incident_channel_ids,
                "incidentProfileId": incident_profile_id,
                "incidentVisibility": incident_visibility,
                "incidentCreationMode": incident_creation_mode,
                "incidentWatchKeys": incident_watch_keys,
            }
        )
        data = {"subscription": subscription}

        res = self._put(f"/api/v1/user/subscriptions/{subscription_id}/", json=data)
        return self._response_to_json(res)

    def delete_subscription(self, *, subscription_id: str) -> dict:
        """Delete a subscription.

        Args:
            subscription_id (str): Subscription ID.

        Returns:
            dict: Empty response object confirming deletion.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/subscriptions/subscriptionsdelete

        """
        res = self._delete(f"/api/v1/user/subscriptions/{subscription_id}/")
        return self._response_to_json(res)

    def get_results(self, *, subscription_id: str, datasource: str) -> dict:
        """Get the search results for a specific subscription and datasource.

        Args:
            subscription_id (str): Subscription ID.
            datasource (str): Datasource (e.g., "scans").

        Returns:
            dict: Search results.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/subscriptions/subscriptionsresults

        """
        return self.get_json(
            f"/api/v1/user/subscriptions/{subscription_id}/results/{datasource}/"
        )
