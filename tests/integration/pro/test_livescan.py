import pytest

from urlscan import Pro


@pytest.mark.integration
def test_get_scanners(pro: Pro):
    scanners = pro.livescan.get_scanners()
    assert isinstance(scanners, dict)
    assert "scanners" in scanners
    assert len(scanners["scanners"]) > 0


@pytest.fixture
def scanner_id() -> str:
    return "us01"


@pytest.mark.integration
def test_scan_get_result_dom_and_purge(pro: Pro, url: str, scanner_id: str):
    # Scan a URL
    result = pro.livescan.scan(url, scanner_id=scanner_id)
    uuid = result["uuid"]

    # Get the result
    scan_result = pro.livescan.get_resource(
        scanner_id=scanner_id, resource_type="result", resource_id=uuid
    )
    assert scan_result is not None

    # Get the DOM
    dom = pro.livescan.get_resource(
        scanner_id=scanner_id, resource_type="dom", resource_id=uuid
    )
    assert dom is not None

    # Purge the scan
    purge_result = pro.livescan.purge(scanner_id=scanner_id, scan_id=uuid)
    assert purge_result is not None
