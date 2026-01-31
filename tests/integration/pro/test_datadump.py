import datetime

import pytest

from urlscan import Pro


@pytest.fixture
def today() -> str:
    return datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y%m%d")


@pytest.mark.integration
def test_datadump_list(pro: Pro, today: str):
    result = pro.datadump.get_list(f"hours/api/{today}")
    assert isinstance(result, dict)
    assert "files" in result
    assert len(result["files"]) > 0


@pytest.mark.integration
def test_datadump_download(pro: Pro, today: str, tmp_path):
    # Download a file from the hours/search path
    output_path = tmp_path / f"{today}.gz"
    with open(output_path, "wb") as f:
        pro.datadump.download_file(
            f"hours/search/{today}/{today}-00.gz",
            file=f,
        )
    assert output_path.exists()
