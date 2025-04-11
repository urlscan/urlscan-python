import logging
import os
import time
from io import BytesIO
from typing import Any, BinaryIO

import httpx
from httpx._types import QueryParamTypes, RequestData, TimeoutTypes

from ._version import version
from .error import APIError, RateLimitError
from .iterator import SearchIterator
from .utils import cast_as_bool

logger = logging.getLogger("urlscan-python")

BASE_URL = os.environ.get("URLSCAN_BASE_URL", "https://urlscan.io")
USER_AGENT = f"urlscan-py/{version}"
RETRY: bool = cast_as_bool(os.environ.get("URLSCAN_RETRY")) or False


def _compact(d: dict) -> dict:
    """Remove empty values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


class RetryTransport(httpx.HTTPTransport):
    def handle_request(self, request: httpx.Request) -> httpx.Response:
        res = super().handle_request(request)
        if res.status_code == 429:
            rate_limit_reset_after: str | None = res.headers.get(
                "X-Rate-Limit-Reset-After"
            )
            if rate_limit_reset_after is None:
                return res

            logger.info(
                f"Rate limit error hit. Wait {rate_limit_reset_after} seconds before retrying..."
            )
            time.sleep(float(rate_limit_reset_after))
            return self.handle_request(request)

        return res


class ClientResponse:
    def __init__(self, res: httpx.Response):
        self._res = res

    @property
    def basename(self) -> str:
        return os.path.basename(self._res.url.path)

    @property
    def content(self) -> bytes:
        return self._res.content

    def json(self) -> Any:
        return self._res.json()

    @property
    def text(self) -> str:
        return self._res.text

    def raise_for_status(self) -> None:
        self._res.raise_for_status()


class Client:
    def __init__(
        self,
        api_key: str,
        base_url: str = BASE_URL,
        user_agent: str = USER_AGENT,
        trust_env: bool = False,
        timeout: TimeoutTypes = 60,
        proxy: str | None = None,
        verify: bool = True,
        retry: bool | None = None,
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
            retry (bool | None, optional): Whether to use automatic X-Rate-Limit-Reset-After HTTP header based retry. Defaults to None.
        """
        self._api_key = api_key
        self._base_url = base_url
        self._user_agent = user_agent
        self._trust_env = trust_env
        self._timeout = timeout
        self._proxy = proxy
        self._verify = verify
        self._retry: bool = retry or RETRY

        self._session: httpx.Client | None = None

    def __enter__(self):
        return self

    def __exit__(self, item_type: Any, value: Any, traceback: Any):
        self.close()

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def _get_session(self) -> httpx.Client:
        if self._session:
            return self._session

        headers = _compact(
            {
                "User-Agent": self._user_agent,
                "API-Key": self._api_key,
            }
        )
        transport: httpx.HTTPTransport | None = None
        if self._retry:
            transport = RetryTransport()

        self._session = httpx.Client(
            base_url=self._base_url,
            headers=headers,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            trust_env=self._trust_env,
            transport=transport,
        )
        return self._session

    def get(self, path: str, params: QueryParamTypes | None = None) -> ClientResponse:
        """Send a GET request to a given API endpoint.

        Args:
            path (str): Path to API endpoint.
            params (QueryParamTypes | None, optional): Query parameters. Defaults to None.

        Returns:
            ClientResponse: Response.
        """
        session = self._get_session()
        return ClientResponse(session.get(path, params=params))

    def get_json(self, path: str, params: QueryParamTypes | None = None) -> dict:
        session = self._get_session()
        res = ClientResponse(session.get(path, params=params))
        return self._response_to_json(res)

    def post(
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
            ClientResponse: _description_
        """
        session = self._get_session()
        return ClientResponse(session.post(path, json=json, data=data))

    def download(
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
        session = self._get_session()
        res = ClientResponse(session.get(path, params=params))
        file.write(res.content)
        return

    def get_content(self, path: str, params: QueryParamTypes | None = None) -> bytes:
        session = self._get_session()
        res = ClientResponse(session.get(path, params=params))
        return self._response_to_content(res)

    def get_text(self, path: str, params: QueryParamTypes | None = None) -> str:
        session = self._get_session()
        res = ClientResponse(session.get(path, params=params))
        return self._response_to_str(res)

    def get_result(self, uuid: str) -> dict:
        """Get a result of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            Dict: Scan result.

        Reference:
            https://urlscan.io/docs/api/#result
        """
        return self.get_json(f"/api/v1/result/{uuid}/")

    def get_screenshot(self, uuid: str) -> BytesIO:
        """Get a screenshot of a scan by UUID.

        Args:
            uuid (str): UUID.

        Returns:
            : Screenshot (img/png) as bytes.

        Reference:
            https://urlscan.io/docs/api/#screenshot
        """
        session = self._get_session()
        res = ClientResponse(session.get(f"/screenshots/{uuid}.png"))
        bio = BytesIO(res.content)
        bio.name = res.basename
        return bio

    def get_dom(self, uuid: str) -> str:
        """Get a DOM of a scan by UUID.

        Args:
            uuid (str): UUID

        Returns:
            str: DOM as a string.

        Reference:
            https://urlscan.io/docs/api/#dom
        """
        return self.get_text(f"/dom/{uuid}/")

    def search(
        self,
        q: str = "",
        size: int = 100,
        limit: int | None = None,
        search_after: str | None = None,
    ) -> SearchIterator:
        """Search.

        Args:
            q (str): Query term. Defaults to "".
            size (int, optional): Number of results returned in a search. Defaults to 100.
            limit (int | None, optional): . Defaults to None.
            search_after (str | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        Returns:
            SearchIterator: Search iterator.
        """
        return SearchIterator(
            self,
            q=q,
            size=size,
            limit=limit,
            search_after=search_after,
        )

    def scan(
        self,
        url: str,
        tags: list[str] | None = None,
        options: dict | None = None,
    ) -> dict:
        """Scan a given URL.

        Args:
            url (str): URL to scan.
            tags (list[str] | None, optional): Tags to be attached. Defaults to None.
            options (dict | None, optional): Options. See https://urlscan.io/docs/api/#submission for details. Defaults to None.

        Returns:
            dict: Scan response.
        """
        data = _compact(
            {
                "url": url,
                "tags": tags,
                "options": options,
            }
        )
        res = self.post("/api/v1/scan/", json=data)
        return self._response_to_json(res)

    def _get_error(self, res: ClientResponse) -> APIError | None:
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as exc:
            data: dict = exc.response.json()
            message: str = data["message"]
            description: str | None = data.get("description")
            status: int = data["status"]

            # ref. https://urlscan.io/docs/api/#ratelimit
            if status == 429:
                rate_limit_reset_after = float(
                    exc.response.headers.get("X-Rate-Limit-Reset-After", 0)
                )
                return RateLimitError(
                    message,
                    description=description,
                    status=status,
                    rate_limit_reset_after=rate_limit_reset_after,
                )

            return APIError(message, description=description, status=status)

        return None

    def _response_to_json(self, res: ClientResponse) -> dict:
        error = self._get_error(res)
        if error:
            raise error

        return res.json()

    def _response_to_str(self, res: ClientResponse) -> str:
        error = self._get_error(res)
        if error:
            raise error

        return res.text

    def _response_to_content(self, res: ClientResponse) -> bytes:
        error = self._get_error(res)
        if error:
            raise error

        return res.content
