import datetime

import pytest

from urlscan.utils import parse_datetime


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
