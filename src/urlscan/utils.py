import datetime


def _compact(d: dict) -> dict:
    """Remove empty values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


def parse_datetime(s: str) -> datetime.datetime:
    dt = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=datetime.timezone.utc)
