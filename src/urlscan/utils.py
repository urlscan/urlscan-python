"""Utility functions for urlscan.io API client."""

import datetime
import gzip
import os
import tarfile

StrOrBytesPath = str | bytes | os.PathLike[str] | os.PathLike[bytes]


def _compact(d: dict) -> dict:
    """Remove empty values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


def parse_datetime(s: str) -> datetime.datetime:
    """Parse an ISO 8601 datetime string to a datetime object."""
    dt = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=datetime.timezone.utc)


def extract(path: StrOrBytesPath, outdir: StrOrBytesPath):
    """Extract a compressed file to the specified output directory."""
    basename = os.path.basename(str(path))
    if basename.endswith(".tar.gz"):
        with tarfile.open(path, mode="r:*", ignore_zeros=True) as tar:
            tar.extractall(outdir)

        return

    if basename.endswith(".gz"):
        filename = basename.removesuffix(".gz")

        with (
            gzip.open(path, "rb") as f_in,
            open(os.path.join(str(outdir), filename), "wb") as f_out,
        ):
            f_out.write(f_in.read())

        return

    raise ValueError(f"Unsupported file type: {basename}")
