"""Notification channel API client module."""

from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import (
    ChannelPermissionType,
    ChannelTypeType,
    FrequencyType,
    WeekDaysType,
)


class Channel(BaseClient):
    """Client API client."""

    def get_channels(self) -> dict:
        """Get a list of notification channels for the current user.

        Returns:
            dict: Object containing an array of channels.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/channels/channels

        """
        return self.get_json("/api/v1/user/channels/")

    def create(
        self,
        *,
        channel_type: ChannelTypeType,
        name: str,
        webhook_url: str | None = None,
        frequency: FrequencyType | None = None,
        email_addresses: list[str] | None = None,
        utc_time: str | None = None,
        is_active: bool | None = None,
        is_default: bool | None = None,
        ignore_time: bool | None = None,
        week_days: list[WeekDaysType] | None = None,
        permissions: list[ChannelPermissionType] | None = None,
    ) -> dict:
        """Create a new channel.

        Args:
            channel_type (ChannelTypeType): Type of channel ("webhook" or "email").
            name (str): Name of the channel.
            webhook_url (str | None, optional): Webhook URL receiving notifications (required when channel_type is "webhook"). Defaults to None.
            frequency (FrequencyType | None, optional): Frequency of notifications ("live", "hourly", or "daily"). Defaults to None.
            email_addresses (list[str] | None, optional): Email addresses receiving the notifications (required when channel_type is "email"). Defaults to None.
            utc_time (str | None, optional): 24 hour UTC time that daily emails are sent (e.g. 09:00). Defaults to None.
            is_active (bool | None, optional): Whether the channel is active. Defaults to None.
            is_default (bool | None, optional): Whether the channel is the default. Defaults to None.
            ignore_time (bool | None, optional): Whether to ignore time constraints. Defaults to None.
            week_days (list[WeekDaysType] | None, optional): Days of the week alerts will be generated (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). Defaults to None.
            permissions (list[ChannelPermissionType] | None, optional): Permissions associated with this channel (team:read, team:write). Defaults to None.

        Returns:
            dict: Object containing the created channel.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/channels/channelscreate

        """
        channel: dict[str, Any] = _compact(
            {
                "type": channel_type,
                "name": name,
                "webhookURL": webhook_url,
                "frequency": frequency,
                "emailAddresses": email_addresses,
                "utcTime": utc_time,
                "isActive": is_active,
                "isDefault": is_default,
                "ignoreTime": ignore_time,
                "weekDays": week_days,
                "permissions": permissions,
            }
        )
        data = {"channel": channel}

        res = self._post("/api/v1/user/channels/", json=data)
        return self._response_to_json(res)

    def get(self, channel_id: str) -> dict:
        """Get the search results for a specific notification channel.

        Args:
            channel_id (str): Channel ID.

        Returns:
            dict: Object containing the channel.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/channels/channelsget

        """
        return self.get_json(f"/api/v1/user/channels/{channel_id}/")

    def update(
        self,
        channel_id: str,
        *,
        channel_type: ChannelTypeType,
        name: str,
        webhook_url: str | None = None,
        frequency: FrequencyType | None = None,
        email_addresses: list[str] | None = None,
        utc_time: str | None = None,
        is_active: bool | None = None,
        is_default: bool | None = None,
        ignore_time: bool | None = None,
        week_days: list[WeekDaysType] | None = None,
        permissions: list[ChannelPermissionType] | None = None,
    ) -> dict:
        """Update an existing channel.

        Args:
            channel_id (str): Channel ID.
            channel_type (ChannelTypeType): Type of channel ("webhook" or "email").
            name (str): Name of the channel.
            webhook_url (str | None, optional): Webhook URL receiving notifications (required when channel_type is "webhook"). Defaults to None.
            frequency (FrequencyType | None, optional): Frequency of notifications ("live", "hourly", or "daily"). Defaults to None.
            email_addresses (list[str] | None, optional): Email addresses receiving the notifications (required when channel_type is "email"). Defaults to None.
            utc_time (str | None, optional): 24 hour UTC time that daily emails are sent (e.g. 09:00). Defaults to None.
            is_active (bool | None, optional): Whether the channel is active. Defaults to None.
            is_default (bool | None, optional): Whether the channel is the default. Defaults to None.
            ignore_time (bool | None, optional): Whether to ignore time constraints. Defaults to None.
            week_days (list[WeekDaysType] | None, optional): Days of the week alerts will be generated (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday). Defaults to None.
            permissions (list[ChannelPermissionType] | None, optional): Permissions associated with this channel (team:read, team:write). Defaults to None.

        Returns:
            dict: Object containing the updated channel.


        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/channels/channelsupdate

        """
        channel: dict[str, Any] = _compact(
            {
                "type": channel_type,
                "name": name,
                "webhookURL": webhook_url,
                "frequency": frequency,
                "emailAddresses": email_addresses,
                "utcTime": utc_time,
                "isActive": is_active,
                "isDefault": is_default,
                "ignoreTime": ignore_time,
                "weekDays": week_days,
                "permissions": permissions,
            }
        )
        data = {"channel": channel}

        res = self._put(f"/api/v1/user/channels/{channel_id}/", json=data)
        return self._response_to_json(res)
