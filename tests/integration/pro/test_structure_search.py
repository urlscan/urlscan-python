import pytest

from urlscan import Pro

# Reference UUID from urlscan.io documentation
# https://docs.urlscan.io/apis/urlscan-openapi/search/similarsearch
REFERENCE_UUID = "68e26c59-2eae-437b-aeb1-cf750fafe7d7"


@pytest.mark.integration
def test_structure_search(pro: Pro):
    it = pro.structure_search(REFERENCE_UUID, size=10, limit=10)
    results = list(it)
    assert len(results) >= 1


@pytest.mark.integration
def test_structure_search_with_query(pro: Pro):
    it = pro.structure_search(REFERENCE_UUID, q="page.domain:*", size=10, limit=10)
    results = list(it)
    assert len(results) >= 1
