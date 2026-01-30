import os

import pytest

from urlscan import Pro


@pytest.fixture
def channel_id() -> str:
    """Get channel ID from environment variable.

    Set CHANNEL_ID environment variable to test channel operations.
    """
    channel_id = os.getenv("CHANNEL_ID")
    if not channel_id:
        pytest.skip("CHANNEL_ID environment variable not set")

    return channel_id


@pytest.mark.integration
def test_get_channels(pro: Pro):
    channels = pro.channel.get_channels()
    assert isinstance(channels, dict)
    assert "channels" in channels
    assert len(channels["channels"]) > 0


@pytest.mark.integration
def test_get_channel(pro: Pro, channel_id: str):
    channel = pro.channel.get(channel_id)
    assert channel is not None
    assert "channel" in channel


@pytest.mark.integration
def test_update_channel(pro: Pro, channel_id: str):
    # Get the current channel details
    channel = pro.channel.get(channel_id)
    original_name = channel["channel"]["name"]
    channel_type = channel["channel"]["type"]

    try:
        # Update the channel name
        updated = pro.channel.update(
            channel_id, channel_type=channel_type, name="integration-test"
        )
        assert updated is not None

        # Verify the update
        retrieved = pro.channel.get(channel_id)
        assert retrieved["channel"]["name"] == "integration-test"

    finally:
        # Revert the change
        pro.channel.update(channel_id, channel_type=channel_type, name=original_name)
