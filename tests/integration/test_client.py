import pytest

from urlscan import Client


@pytest.mark.integration
def test_scan_and_get_result(client: Client, url: str):
    result = client.scan(url, visibility="private")
    uuid: str = result["uuid"]
    client.wait_for_result(uuid)

    assert client.get_dom(uuid) is not None
    assert client.get_screenshot(uuid) is not None
    assert client.get_result(uuid) is not None


@pytest.mark.integration
def test_search_with_limit(client: Client):
    it = client.search("page.domain:example.com", limit=1)
    results = list(it)
    assert len(results) == 1


@pytest.mark.integration
def test_search_with_limit_and_size(client: Client):
    it = client.search("page.domain:example.com", limit=10, size=5)
    results = list(it)
    assert len(results) == 10


@pytest.mark.integration
def test_quotas(client: Client):
    quotas = client.get_quotas()
    assert quotas["scope"] in ("team", "user")


@pytest.mark.integration
def test_get_available_countries(client: Client):
    countries = client.get_available_countries()
    assert isinstance(countries, dict)
    assert len(countries) > 0


@pytest.mark.integration
def test_get_user_agents(client: Client):
    user_agents = client.get_user_agents()
    assert isinstance(user_agents, dict)
    assert len(user_agents) > 0
