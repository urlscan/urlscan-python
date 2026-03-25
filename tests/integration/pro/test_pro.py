import pytest

from urlscan import Pro


@pytest.mark.integration
def test_lookup_malicious_observable(pro: Pro):
    type_ = "url"
    value = "https://example.com"
    result = pro.lookup_malicious_observable(type_="url", value=value)
    assert isinstance(result, dict)
    assert result["type"] == type_
    assert result["observable"] in value
