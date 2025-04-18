import asyncio
from io import BytesIO
from typing import Any, BinaryIO

import httpx
from httpx._types import QueryParamTypes, RequestData, TimeoutTypes

from urlscan.types import VisibilityType

from .base import (
    BASE_URL,
    USER_AGENT,
    BaseClient,
    ClientResponse,
    _compact,
    logger,
)
from .iterator import AsyncSearchIterator


class AsyncRetryTransport(httpx.AsyncHTTPTransport):
    async def handle_request(self, request: httpx.Request) -> httpx.Response:
        res = await super().handle_async_request(request)
        if res.status_code == 429:
            rate_limit_reset_after: str | None = res.headers.get(
                "X-Rate-Limit-Reset-After"
            )
            if rate_limit_reset_after is None:
                return res

            logger.info(
                f"Rate limit error hit. Wait {rate_limit_reset_after} seconds before retrying..."
            )
            await asyncio.sleep(float(rate_limit_reset_after))
            return await self.handle_async_request(request)

        return res


class AsyncClient(BaseClient):
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        user_agent: str = USER_AGENT,
        trust_env: bool = False,
        timeout: TimeoutTypes = 60,
        proxy: str | None = None,
        verify: bool = True,
        retry: bool = False,
    ):
        """
        Args:
            api_key (str): Your urlscan.io API key.
            base_url (str, optional): Base URL. Defaults to BASE_URL.
            user_agent (str, optional): User agent. Defaults to USER_AGENT.
            trust_env (bool, optional): Enable or disable usage of environment variables for configuration. Defaults to False.
            timeout (TimeoutTypes, optional): timeout configuration to use when sending request. Defaults to 60.
            proxy (str | None, optional): Proxy URL where all the traffic should be routed. Defaults to None.
            verify (bool, optional): Either `True` to use an SSL context with the default CA bundle, `False` to disable verification. Defaults to True.
            retry (bool, optional): Whether to use automatic X-Rate-Limit-Reset-After HTTP header based retry. Defaults to False.
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            user_agent=user_agent,
            trust_env=trust_env,
            timeout=timeout,
            proxy=proxy,
            verify=verify,
            retry=retry,
        )

        self._session: httpx.AsyncClient | None = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, item_type: Any, value: Any, traceback: Any):
        await self.close()

    async def close(self):
        if self._session:
            await self._session.aclose()
            self._session = None

    def _get_session(self) -> httpx.AsyncClient:
        if self._session:
            return self._session

        headers = _compact(
            {
                "User-Agent": self._user_agent,
                "API-Key": self._api_key,
            }
        )
        transport: httpx.AsyncHTTPTransport | None = None
        if self._retry:
            transport = AsyncRetryTransport()

        self._session = httpx.AsyncClient(
            base_url=self._base_url,
            headers=headers,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            trust_env=self._trust_env,
            transport=transport,
        )
        return self._session

    async def _send_request(
        self, session: httpx.AsyncClient, request: httpx.Request
    ) -> ClientResponse:
        if self._retry:
            return ClientResponse(await session.send(request))

        self._check_before_action(request)
        res = ClientResponse(await session.send(request))
        self._check_after_action(res)

        return res

    async def get(
        self, path: str, params: QueryParamTypes | None = None
    ) -> ClientResponse:
        """Send a GET request to a given API endpoint.

        Args:
            path (str): Path to API endpoint.
            params (QueryParamTypes | None, optional): Query parameters. Defaults to None.

        Returns:
            ClientResponse: Response.
        """
        session = self._get_session()
        req = session.build_request("GET", path, params=params)
        return await self._send_request(session, req)

    async def get_json(self, path: str, params: QueryParamTypes | None = None) -> dict:
        res = await self.get(path, params=params)
        return self._response_to_json(res)

    async def post(
        self,
        path: str,
        json: Any | None = None,
        data: RequestData | None = None,
    ) -> ClientResponse:
        """Send a POST request to a given API endpoint.

        Args:
            path (str): Path.
            json (Any | None, optional): Dict to send in request body as JSON. Defaults to None.
            data (RequestData | None, optional): Dict to send in request body. Defaults to None.

        Returns:
            ClientResponse: Response.
        """
        session = self._get_session()
        req = session.build_request("POST", path, json=json, data=data)
        return await self._send_request(session, req)

    async def download(
        self,
        path: str,
        file: BinaryIO,
        params: QueryParamTypes | None = None,
    ) -> None:
        """Download a file from a given API endpoint.

        Args:
            path (str): Path to API endpoint.
            file (BinaryIO): File object to write to.
            params (QueryParamTypes | None, optional): Query parameters. Defaults to None.

        Returns:
            BytesIO: File content.
        """
        res = await self.get(path, params=params)
        file.write(res.content)
        return

    async def get_content(
        self, path: str, params: QueryParamTypes | None = None
    ) -> bytes:
        res = await self.get(path, params=params)
        return self._response_to_content(res)

    async def get_text(self, path: str, params: QueryParamTypes | None = None) -> str:
        res = await self.get(path, params=params)
        return self._response_to_str(res)

    async def get_result(self, uuid: str) -> dict:
        """Get a result of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            Dict: Scan result.

        Reference:
            https://urlscan.io/docs/api/#result
        """
        return await self.get_json(f"/api/v1/result/{uuid}/")

    async def get_screenshot(self, uuid: str) -> BytesIO:
        """Get a screenshot of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            : Screenshot (img/png) as bytes.

        Reference:
            https://urlscan.io/docs/api/#screenshot
        """
        res = await self.get(f"/screenshots/{uuid}.png")
        bio = BytesIO(res.content)
        bio.name = res.basename
        return bio

    async def get_dom(self, uuid: str) -> str:
        """Get a DOM of a scan by UUID.

        Args:
            uuid (str): UUID

        Returns:
            str: DOM as a string.

        Reference:
            https://urlscan.io/docs/api/#dom
        """
        return await self.get_text(f"/dom/{uuid}/")

    def search(
        self,
        q: str = "",
        size: int = 100,
        limit: int | None = None,
        search_after: str | None = None,
    ) -> AsyncSearchIterator:
        """Search.

        Args:
            q (str): Query term. Defaults to "".
            size (int, optional): Number of results returned in a search. Defaults to 100.
            limit (int | None, optional): . Defaults to None.
            search_after (str | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        Returns:
            AsyncSearchIterator: Search iterator.

        Reference:
            https://urlscan.io/docs/api/#search
        """
        return AsyncSearchIterator(
            self,
            q=q,
            size=size,
            limit=limit,
            search_after=search_after,
        )

    async def scan(
        self,
        url: str,
        *,
        visibility: VisibilityType,
        tags: list[str] | None = None,
        customagent: str | None = None,
        referer: str | None = None,
        override_safety: Any = None,
        country: str | None = None,
    ) -> dict:
        """Scan a given URL.

        Args:
            url (str): URL to scan.
            visibility (VisibilityType): Visibility of the scan. Can be "public", "private", or "unlisted"
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            customagent (str | None, optional): Custom user agent. Defaults to None.
            referer (str | None, optional): Referer. Defaults to None.
            override_safety (Any, optional): If set to any value, this will disable reclassification of URLs with potential PII in them. Defaults to None.
            country (str | None, optional): Specify which country the scan should be performed from (2-Letter ISO-3166-1 alpha-2 country). Defaults to None.

        Returns:
            dict: Scan response.

        Reference:
            https://urlscan.io/docs/api/#scan
        """
        data = _compact(
            {
                "url": url,
                "tags": tags,
                "visibility": visibility,
                "customagent": customagent,
                "referer": referer,
                "overrideSafety": override_safety,
                "country": country,
            }
        )
        res = await self.post("/api/v1/scan/", json=data)
        json_res = self._response_to_json(res)

        json_visibility = json_res.get("visibility")
        if json_visibility is not None and json_visibility != visibility:
            logger.warning(f"Visibility is enforced to {json_visibility}.")

        return json_res
