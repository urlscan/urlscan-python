import pytest

from urlscan import Client, Pro


@pytest.mark.integration
def test_change_and_reset_visibility(client: Client, pro: Pro, url: str):
    result = client.scan(url, visibility="private")
    uuid: str = result["uuid"]
    client.wait_for_result(uuid)

    # Change visibility to public
    res = pro.visibility.update(uuid, "public")
    assert res["uuid"] == uuid
    assert res["visibility"] == "public"

    # Reset visibility to original (private)
    res = pro.visibility.reset(uuid)
    assert res["uuid"] == uuid
