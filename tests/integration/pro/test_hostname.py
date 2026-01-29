import pytest

from urlscan import Pro


@pytest.mark.integration
def test_hostname_with_limit(pro: Pro):
    it = pro.hostname("example.com", limit=1)
    results = list(it)
    assert len(results) == 1


@pytest.mark.integration
def test_hostname_with_limit_and_size(pro: Pro):
    it = pro.hostname("example.com", limit=10, size=10)
    results = list(it)
    assert len(results) == 10
