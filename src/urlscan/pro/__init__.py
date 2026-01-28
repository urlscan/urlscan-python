"""urlscan.io Pro API client module."""

from functools import cached_property
from typing import BinaryIO

from urlscan.client import BaseClient
from urlscan.iterator import SearchIterator
from urlscan.utils import _compact

from .brand import Brand
from .channel import Channel
from .datadump import DataDump
from .hostname import HostnameIterator
from .incident import Incident
from .livescan import LiveScan
from .saved_search import SavedSearch
from .subscription import Subscription


class Pro(BaseClient):
    """urlscan.io Pro API client."""

    @cached_property
    def brand(self) -> Brand:
        """Brand API client instance.

        Returns:
            Brand: Brand API client instance.

        """
        return Brand(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def channel(self) -> Channel:
        """Channel API client instance.

        Returns:
            Channel: Channel API client instance.

        """
        return Channel(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def datadump(self) -> DataDump:
        """Data dump API client instance.

        Returns:
            DataDump: Data dump API client instance.

        """
        return DataDump(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def incident(self) -> Incident:
        """Incident API client instance.

        Returns:
            Incident: Incident API client instance.

        """
        return Incident(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def livescan(self) -> LiveScan:
        """Live scan API client instance.

        Returns:
            LiveScan: Live scan API client instance.

        """
        return LiveScan(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def saved_search(self) -> SavedSearch:
        """Saved Search API client instance.

        Returns:
            SavedSearch: Saved Search API client instance.

        """
        return SavedSearch(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    @cached_property
    def subscription(self) -> Subscription:
        """Subscription API client instance.

        Returns:
            Subscription: Subscription API client instance.

        """
        return Subscription(
            api_key=self._api_key,
            base_url=self._base_url,
            user_agent=self._user_agent,
            trust_env=self._trust_env,
            timeout=self._timeout,
            proxy=self._proxy,
            verify=self._verify,
            retry=self._retry,
        )

    def structure_search(
        self,
        scan_id: str,
        *,
        q: str | None = None,
        size: int = 100,
        search_after: str | None = None,
        limit: int | None = None,
    ) -> SearchIterator:
        """Get results structurally similar to a specific scan.

        Args:
            scan_id (str): The original scan to compare to.
            q (str | None, optional): Additional query filter.
            size (int): Maximum results per call. Defaults to 100.
            search_after (str | None, optional): Parameter to iterate over older results. Defaults to None.
            limit (int | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        """
        return SearchIterator(
            client=self,
            path=f"/api/v1/pro/result/{scan_id}/similar/",
            q=q,
            size=size,
            search_after=search_after,
            limit=limit,
        )

    def hostname(
        self,
        hostname: str,
        *,
        size: int = 1000,
        limit: int | None = None,
        page_state: str | None = None,
    ) -> HostnameIterator:
        """Get the historical observations for a specific hostname.

        Args:
            hostname (str): The hostname to query.
            page_state (str | None, optional): Page state for pagination. Defaults to None.
            size (int, optional): Number of results returned in a search. Defaults to 1000.
            limit (int | None, optional): Maximum number of results that will be returned by the iterator. Defaults to None.

        Returns:
            HostnameIterator: Hostname iterator.

        """
        return HostnameIterator(
            client=self,
            hostname=hostname,
            size=size,
            limit=limit,
            page_state=page_state,
        )

    def download_file(
        self,
        file_hash: str,
        *,
        file: BinaryIO,
        password: str | None = None,
        filename: str | None = None,
    ):
        """Download a file by its hash.

        Examples:
            >>> from urlscan import Pro
            >>> with Pro("<your_api_key>") as pro, open("downloaded_file.zip", "wb") as f:
            ...     pro.download_file(
            ...         file_hash="<file_hash>",
            ...         file=f,
            ...     )

        Args:
            file_hash (str): The hash of the file to download.
            file (BinaryIO): File object to write to.
            password (str | None, optional): The password to use to encrypt the ZIP file. The default password is "urlscan!" if it's not provided. Defaults to None.
            filename (str | None, optional): Specify the name of the ZIP file that should be downloaded. This does not change the name of files within the ZIP archive. The default filename is {file_hash}.zip if it's not provided. Defaults to None.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/files/downloadfile

        """
        params: dict[str, str] = _compact(
            {
                "password": password,
                "filename": filename,
            }
        )
        return self.download(f"/downloads/{file_hash}", params=params, file=file)

    def get_user(self) -> dict:
        """Get information about the current user or API key making the request.

        Returns:
            dict: User information.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/generic/prousername

        """
        return self.get_json("/api/v1/pro/username")
