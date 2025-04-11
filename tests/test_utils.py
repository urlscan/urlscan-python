import pytest

from urlscan.utils import cast_as_bool


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("true", True),
        ("1", True),
        ("false", False),
        ("0", False),
        (None, None),
        ("foo", ValueError),
    ],
)
def test_cast_as_bool(value, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            cast_as_bool(value)
    else:
        assert cast_as_bool(value) == expected
