import datetime
import tempfile
from pathlib import Path

import pytest

from urlscan.utils import extract, parse_datetime


@pytest.mark.parametrize(
    "input_str, expected",
    [
        (
            "2025-04-12T02:11:00.000Z",
            datetime.datetime(2025, 4, 12, 2, 11, 0, tzinfo=datetime.timezone.utc),
        ),
    ],
)
def test_parse_datetime(input_str: str, expected: datetime.datetime):
    result = parse_datetime(input_str)
    assert result == expected


@pytest.fixture
def gz():
    return "tests/unit/fixtures/test.gz"


@pytest.fixture
def tar_gz():
    # this file is created by:
    # $ gtar -cf 1.tar 1.txt
    # $ gtar -cf 2.tar 2.txt
    # $ cat 1.tar 2.tar > test.tar
    # $ gzip test.tar
    return "tests/unit/fixtures/test.tar.gz"


def test_extract_with_gz(gz: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        extract(gz, tmpdir)
        assert set(Path(tmpdir).iterdir()) == {
            Path(tmpdir) / "test",
        }


def test_extract_with_tar_gz(tar_gz: str):
    with tempfile.TemporaryDirectory() as tmpdir:
        extract(tar_gz, tmpdir)
        assert set(Path(tmpdir).iterdir()) == {
            Path(tmpdir) / "1.txt",
            Path(tmpdir) / "2.txt",
        }
