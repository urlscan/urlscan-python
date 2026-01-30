"""Data dump API client module."""

from typing import BinaryIO
from urllib.parse import urljoin

from urlscan.client import BaseClient


class DataDump(BaseClient):
    """Data dump API client."""

    def get_list(self, path: str) -> dict:
        """List available data dump files for a specific time window, file type, and date.

        Args:
            path (str): The data dump path. Format is /{time_window}/{file_type}/{date}/.
                        - time_window: days, hours, minutes.
                        - file_type: api, search, screenshots, dom.
                        - date: date of the data dump in YYYYMMDD format.

        Returns:
            dict: The list of data dump files.

        Examples:
            >>> from urlscan import Pro
            >>> with Pro("<your_api_key>") as client:
            ...     result = client.datadump.get_list("days/api/20260101")

        """
        return self.get_json(urljoin("/api/v1/datadump/list/", path))

    def download_file(
        self,
        path: str,
        file: BinaryIO,
    ):
        """Download the datadump file.

        Args:
            path (str): Path to API endpoint.
            file (BinaryIO): File object to write to.

        """
        return super().download(
            urljoin("/api/v1/datadump/link/", path),
            file=file,
        )
