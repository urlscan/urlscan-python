from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client


class SearchIterator:
    """
    Search iterator.

    Examples:
        >>> from urlscan import Client
        >>>> with Client("<your_api_key>") as client:
        >>>     for result in client.search("page.domain:example.com"):
        >>>         print(result["_id"], result["page"]["url"])
    """

    def __init__(
        self,
        client: "Client",
        *,
        q: str,
        search_after: str | None = None,
        size: int = 100,
        limit: int | None = None,
    ):
        """
        Args:
            client (Client): Client.
            q (str): Search query.
            search_after (str | None, optional): Search after to retrieve next results. Defaults to None.
            size (int, optional): Number of results returned in a search. Defaults to 100.
            limit (int | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.
        """
        self._client = client
        self._size = size
        self._q = q
        self._search_after = search_after

        self._results: list[dict] = []
        self._limit = limit
        self._has_more = True
        self._count = 0

    def _parse_response(self, data: dict):
        results: list[dict] = data["results"]
        has_more: bool = data["has_more"]
        return results, has_more

    def _get(self):
        data = self._client.get_json(
            "/api/v1/search/",
            params={
                "q": self._q,
                "size": self._size,
                "search_after": self._search_after,
            },
        )
        return self._parse_response(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self._limit and self._count >= self._limit:
            raise StopIteration()

        if not self._results and (self._count == 0 or self._has_more):
            self._results, self._has_more = self._get()
            if len(self._results) > 0:
                last_result = self._results[-1]
                sort: list[str | int] = last_result["sort"]
                self._search_after = ",".join(str(x) for x in sort)

        if not self._results:
            raise StopIteration()

        result = self._results.pop(0)
        self._count += 1
        return result
