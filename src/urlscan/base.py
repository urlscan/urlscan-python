import contextlib
import datetime
import json
import logging
import os
from dataclasses import dataclass
from typing import Any, TypedDict

import httpx
from httpx._types import TimeoutTypes

from ._version import version
from .error import APIError, RateLimitError, RateLimitRemainingError
from .types import ActionType
from .utils import parse_datetime

logger = logging.getLogger("urlscan-python")

BASE_URL = os.environ.get("URLSCAN_BASE_URL", "https://urlscan.io")
USER_AGENT = f"urlscan-py/{version}"


def _compact(d: dict) -> dict:
    """Remove empty values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


@dataclass
class RateLimit:
    remaining: int
    reset: datetime.datetime


class RateLimitMemo(TypedDict):
    public: RateLimit | None
    private: RateLimit | None
    unlisted: RateLimit | None
    retrieve: RateLimit | None
    search: RateLimit | None


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

    @property
    def headers(self):
        return self._res.headers

    def raise_for_status(self) -> None:
        self._res.raise_for_status()


class BaseClient:
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
        self._api_key = api_key
        self._base_url = base_url
        self._user_agent = user_agent
        self._trust_env = trust_env
        self._timeout = timeout
        self._proxy = proxy
        self._verify = verify
        self._retry = retry

        self._rate_limit_memo: RateLimitMemo = {
            "public": None,
            "private": None,
            "unlisted": None,
            "retrieve": None,
            "search": None,
        }

    def _get_action(self, request: httpx.Request) -> ActionType | None:
        path = request.url.path
        if request.method == "GET":
            if path == "/api/v1/search/":
                return "search"

            if path.startswith("/api/v1/result/"):
                return "retrieve"

            return None

        if request.method == "POST":
            if path != "/api/v1/scan/":
                return None

            if request.headers.get("Content-Type") != "application/json":
                return None

            with contextlib.suppress(json.JSONDecodeError):
                data: dict = json.loads(request.content)
                return data.get("visibility")

        return None

    def _check_before_action(self, request: httpx.Request) -> None:
        action = self._get_action(request)
        if action:
            rate_limit: RateLimit | None = self._rate_limit_memo.get(action)
            if rate_limit:
                utcnow = datetime.datetime.now(datetime.timezone.utc)
                if rate_limit.remaining == 0 and rate_limit.reset > utcnow:
                    raise RateLimitRemainingError(
                        f"{action} is rate limited. Wait until {utcnow}."
                    )

    def _check_after_action(self, res: ClientResponse) -> None:
        # use action in response headers
        action = res.headers.get("X-Rate-Limit-Action")
        if action:
            remaining = res.headers.get("X-Rate-Limit-Remaining")
            reset = res.headers.get("X-Rate-Limit-Reset")
            if remaining and reset:
                self._rate_limit_memo[action] = RateLimit(  # type: ignore
                    remaining=int(remaining),
                    reset=parse_datetime(reset),
                )

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
