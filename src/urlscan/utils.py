import datetime


def parse_datetime(s: str) -> datetime.datetime:
    dt = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=datetime.timezone.utc)
