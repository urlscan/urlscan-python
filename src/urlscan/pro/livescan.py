"""Live scanning API client module."""

from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import LiveScanResourceType, VisibilityType
from urlscan.utils import _merge

DEPRECATED_FEATURES: set[str] = {"stealth"}


class LiveScan(BaseClient):
    """Live scanning API client."""

    def get_scanners(self) -> dict:
        """Get a list of available Live Scanning nodes along with their current metadata.

        Returns:
            dict: List of available scanners with metadata.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescanscanners

        """
        return self.get_json("/api/v1/livescan/scanners/")

    def _build_scan_payload(
        self,
        url: str,
        visibility: VisibilityType | None = None,
        page_timeout: int | None = None,
        capture_delay: int | None = None,
        extra_headers: dict[str, str] | None = None,
        enable_features: list[str] | None = None,
        disable_features: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Build the payload for a scan request."""
        task: dict[str, Any] = _compact(
            {
                "url": url,
                "visibility": visibility,
            }
        )
        # check for deprecated features
        for feature in disable_features or []:
            if feature in DEPRECATED_FEATURES:
                self._warn_deprecation(
                    f"The feature '{feature}' is deprecated.", stacklevel=4
                )
        scanner: dict[str, Any] = _compact(
            _merge(
                {
                    "pageTimeout": page_timeout,
                    "captureDelay": capture_delay,
                    "extraHeaders": extra_headers,
                    "enableFeatures": enable_features,
                    "disableFeatures": disable_features,
                },
                kwargs,
            )
        )
        return {"task": task, "scanner": scanner}

    def task(
        self,
        url: str,
        *,
        scanner_id: str,
        visibility: VisibilityType | None = None,
        page_timeout: int | None = None,
        capture_delay: int | None = None,
        extra_headers: dict[str, str] | None = None,
        enable_features: list[str] | None = None,
        disable_features: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        """Task a URL to be scanned.

        The HTTP request will return with the scan UUID immediately and then it is your responsibility to poll the result resource type until the scan has finished.

        Args:
            url (str): URL to scan.
            scanner_id (str): Scanner ID (e.g., "de01" for Germany).
            visibility (VisibilityType | None, optional): Visibility of the scan. Defaults to None.
            page_timeout (int | None, optional): Time to wait for the whole scan process (in ms). Defaults to None.
            capture_delay (int | None, optional): Delay after page load before capturing (in ms). Defaults to None.
            extra_headers (dict[str, str] | None, optional): Extra HTTP headers. Defaults to None.
            enable_features (list[str] | None, optional): Features to enable. Defaults to None.
            disable_features (list[str] | None, optional): Features to disable. Defaults to None.
            **kwargs: Additional parameters to include in the request payload.

        Returns:
            dict: Response containing the scan UUID.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescantask

        """
        data = self._build_scan_payload(
            url,
            visibility=visibility,
            page_timeout=page_timeout,
            capture_delay=capture_delay,
            extra_headers=extra_headers,
            enable_features=enable_features,
            disable_features=disable_features,
            **kwargs,
        )
        res = self._post(f"/api/v1/livescan/{scanner_id}/task/", json=data)
        return self._response_to_json(res)

    def scan(
        self,
        url: str,
        *,
        scanner_id: str,
        visibility: VisibilityType | None = None,
        page_timeout: int | None = None,
        capture_delay: int | None = None,
        extra_headers: dict[str, str] | None = None,
        enable_features: list[str] | None = None,
        disable_features: list[str] | None = None,
        **kwargs: Any,
    ) -> dict:
        """Task a URL to be scanned. The HTTP request will block until the scan has finished.

        Args:
            url (str): URL to scan.
            scanner_id (str): Scanner ID (e.g., "de01" for Germany).
            visibility (VisibilityType | None, optional): Visibility of the scan. Defaults to None.
            page_timeout (int | None, optional): Time to wait for the whole scan process (in ms). Defaults to None.
            capture_delay (int | None, optional): Delay after page load before capturing (in ms). Defaults to None.
            extra_headers (dict[str, str] | None, optional): Extra HTTP headers. Defaults to None.
            enable_features (list[str] | None, optional): Features to enable. Defaults to None.
            disable_features (list[str] | None, optional): Features to disable. Defaults to None.
            **kwargs: Additional parameters to include in the request payload.

        Returns:
            dict: Response containing the scan UUID.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescanscan

        """
        data = self._build_scan_payload(
            url,
            visibility=visibility,
            page_timeout=page_timeout,
            capture_delay=capture_delay,
            extra_headers=extra_headers,
            enable_features=enable_features,
            disable_features=disable_features,
            **kwargs,
        )
        res = self._post(f"/api/v1/livescan/{scanner_id}/scan/", json=data)
        return self._response_to_json(res)

    def get_resource(
        self,
        *,
        scanner_id: str,
        resource_type: LiveScanResourceType,
        resource_id: str,
    ) -> Any:
        """Retrieve the resource for a particular scan ID or SHA256 from this live scanner.

        Args:
            scanner_id (str): Scanner ID (e.g., "de01" for Germany).
            resource_type (LiveScanResourceType): Type of resource ("result", "screenshot", "dom", "response", or "download").
            resource_id (str): Resource ID. For result/screenshot/dom: UUID of the scan. For response/download: SHA256 of the resource.

        Returns:
            Any: Resource content. Returns dict for "result", str for "dom", bytes for binary resources.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescangetresource

        """
        path = f"/api/v1/livescan/{scanner_id}/{resource_type}/{resource_id}"

        if resource_type == "result":
            return self.get_json(path)

        if resource_type in ("screenshot", "response", "download"):
            return self.get_content(path)

        if resource_type == "dom":
            return self.get_text(path)

        return self._get(path)

    def store(
        self,
        *,
        scanner_id: str,
        scan_id: str,
        visibility: VisibilityType,
    ) -> dict:
        """Store the temporary scan as a permanent snapshot on urlscan.io.

        Args:
            scanner_id (str): Scanner ID (e.g., "de01" for Germany).
            scan_id (str): Scan UUID.
            visibility (VisibilityType): Visibility for the stored scan ("public", "private", or "unlisted").

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescanstore

        """
        data = {"task": {"visibility": visibility}}
        res = self._put(f"/api/v1/livescan/{scanner_id}/{scan_id}/", json=data)
        return self._response_to_json(res)

    def purge(
        self,
        *,
        scanner_id: str,
        scan_id: str,
    ) -> dict:
        """Purge temporary scan from scanner immediately. Scans will be automatically purged after 60 minutes.

        Args:
            scanner_id (str): Scanner ID (e.g., "de01" for Germany).
            scan_id (str): Scan UUID.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/live-scanning/livescandiscard

        """
        res = self._delete(f"/api/v1/livescan/{scanner_id}/{scan_id}/")
        return self._response_to_json(res)
