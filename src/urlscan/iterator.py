from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .async_client import AsyncClient
    from .client import Client


class BaseSearchIterator:
    def __init__(
        self,
        *,
        q: str,
        search_after: str | None = None,
        size: int = 100,
        limit: int | None = None,
    ):
        self._size = size
        self._q = q
        self._search_after = search_after

        self._results: list[dict] = []
        self._limit = limit
        self._has_more = True
        self._count = 0

    def _parse_response(self, data: dict) -> tuple[list[dict], bool]:
        results: list[dict] = data["results"]
        has_more: bool = data["has_more"]
        return results, has_more

    def _update_search_after(self):
        if len(self._results) > 0:
            last_result = self._results[-1]
            sort: list[str | int] = last_result["sort"]
            self._search_after = ",".join(str(x) for x in sort)


class SearchIterator(BaseSearchIterator):
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
        super().__init__(q=q, search_after=search_after, size=size, limit=limit)
        self._client = client

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
            self._update_search_after()

        if not self._results:
            raise StopIteration()

        result = self._results.pop(0)
        self._count += 1
        return result


class AsyncSearchIterator(BaseSearchIterator):
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
        client: "AsyncClient",
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
        super().__init__(q=q, search_after=search_after, size=size, limit=limit)
        self._client = client

    async def _get(self):
        data = await self._client.get_json(
            "/api/v1/search/",
            params={
                "q": self._q,
                "size": self._size,
                "search_after": self._search_after,
            },
        )
        return self._parse_response(data)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._limit and self._count >= self._limit:
            raise StopAsyncIteration()

        if not self._results and (self._count == 0 or self._has_more):
            self._results, self._has_more = await self._get()
            self._update_search_after()

        if not self._results:
            raise StopAsyncIteration()

        result = self._results.pop(0)
        self._count += 1
        return result
