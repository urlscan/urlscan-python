"""Iterator classes for paginated API responses."""

from typing import TYPE_CHECKING

from .types import SearchDataSource
from .utils import _compact

if TYPE_CHECKING:
    from .client import BaseClient

MAX_TOTAL = 10_000


class BaseIterator:
    """Base iterator."""

    def __iter__(self):
        """Return the iterator object."""
        return self

    def __next__(self):
        """Return the next item from the iterator."""
        raise NotImplementedError()


class SearchIterator(BaseIterator):
    """Search iterator.

    Examples:
        >>> from urlscan import Client
        >>> with Client("<your_api_key>") as client:
        ...     for result in client.search("page.domain:example.com"):
        ...         print(result["_id"], result["page"]["url"])

    """

    def __init__(
        self,
        client: "BaseClient",
        *,
        path: str,
        q: str | None = None,
        search_after: str | None = None,
        size: int = 100,
        limit: int | None = None,
        datasource: SearchDataSource | None = None,
        collapse: str | None = None,
    ):
        """Initialize the search iterator.

        Args:
            client (Client): Client.
            path (str): API path for the search endpoint.
            q (str | None, optional): Search query. Defaults to None.
            search_after (str | None, optional): Search after to retrieve next results. Defaults to None.
            size (int, optional): Number of results returned in a search. Defaults to 100.
            limit (int | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.
            datasource (SearchDataSource | None, optional): Datasources to search: scans (urlscan.io), hostnames, incidents, notifications, certificates (urlscan Pro). Defaults to None.
            collapse (str | None, optional): Field to collapse results on. Only works on current page of results. Defaults to None.

        """
        self._client = client
        self._path = path
        self._size = size
        self._q = q
        self._search_after = search_after
        self._datasource = datasource
        self._collapse = collapse

        self._results: list[dict] = []
        self._limit = limit
        self._count = 0
        self._total: int | None = None
        self._has_more: bool = True

    def _parse_response(self, data: dict) -> tuple[list[dict], int]:
        results: list[dict] = data["results"]
        total: int = data["total"]
        return results, total

    def _get(self):
        data = self._client.get_json(
            self._path,
            params=_compact(
                {
                    "q": self._q,
                    "size": self._size,
                    "search_after": self._search_after,
                    "datasource": self._datasource,
                    "collapse": self._collapse,
                }
            ),
        )
        return self._parse_response(data)

    def __iter__(self):
        """Return the iterator object."""
        return self

    def __next__(self):
        """Return the next search result."""
        if self._limit and self._count >= self._limit:
            raise StopIteration()

        if not self._results and (self._count == 0 or self._has_more):
            self._results, total = self._get()

            # NOTE: total should be set only once (to ignore newly added results after the first request)
            self._total = self._total or total
            if self._total != MAX_TOTAL:
                self._has_more = self._total > (self._count + len(self._results))
            else:
                self._has_more = len(self._results) >= self._size

            if len(self._results) > 0:
                last_result = self._results[-1]
                sort: list[str | int] = last_result["sort"]
                self._search_after = ",".join(str(x) for x in sort)

        if not self._results:
            raise StopIteration()

        result = self._results.pop(0)
        self._count += 1
        return result
