"""Hostname API client module."""

from urllib.parse import urljoin

from urlscan.client import BaseClient
from urlscan.iterator import BaseIterator
from urlscan.utils import _compact


class HostnameIterator(BaseIterator):
    """Hostname iterator.

    Examples:
        >>> from urlscan import Pro
        >>> with Pro("<your_api_key>") as client:
        >>>     for result in client.hostname("example.com"):
        >>>         print(result["sub_id"], result["data"])

    """

    def __init__(
        self,
        client: BaseClient,
        *,
        hostname: str,
        page_state: str | None = None,
        size: int = 1_000,
        limit: int | None = None,
    ):
        """Initialize the hostname iterator.

        Args:
            client (Client): Client.
            hostname (str): Hostname to query.
            page_state (str | None, optional): Page state for pagination. Defaults to None.
            size (int, optional): Number of results returned in a search. Defaults to 1000.
            limit (int | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        """
        self._client = client
        self._path = urljoin("/api/v1/hostname/", hostname)
        self._page_state = page_state
        self._size = size
        self._results: list[dict] = []
        self._limit = limit
        self._count = 0
        self._has_more: bool = True

    def _parse_response(self, data: dict) -> tuple[list[dict], str | None]:
        results: list[dict] = data["results"]
        page_state: str | None = data["pageState"]
        return results, page_state

    def _get(self):
        data = self._client.get_json(
            self._path,
            params=_compact(
                {
                    "limit": self._size,
                    "pageState": self._page_state,
                }
            ),
        )
        return self._parse_response(data)

    def __next__(self):
        """Return the next hostname observation result."""
        if self._limit and self._count >= self._limit:
            raise StopIteration()

        if len(self._results) == 0 and self._has_more:
            self._results, page_state = self._get()
            self._page_state = page_state
            self._has_more = page_state is not None

        if len(self._results) == 0:
            raise StopIteration()

        result = self._results.pop(0)
        self._count += 1
        return result
