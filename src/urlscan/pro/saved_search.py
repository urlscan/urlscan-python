from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import PermissionType, SavedSearchDataSource, TLPType


class SavedSearch(BaseClient):
    def get_list(self) -> dict:
        """Get a list of saved searches.

        Returns:
            dict: List of saved searches.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-get
        """
        return self.get_json("/api/v1/user/searches/")

    def create(
        self,
        *,
        datasource: SavedSearchDataSource,
        query: str,
        name: str,
        description: str | None = None,
        long_description: str | None = None,
        tlp: TLPType | None = None,
        user_tags: list[str] | None = None,
        permissions: list[PermissionType] | None = None,
    ) -> dict:
        """Create a new saved search.

        Args:
            datasource (SavedSearchDataSource): Data source to search ("hostnames" or "scans").
            query (str): Search API query string.
            name (str): User-facing name for the saved search.
            description (str | None, optional): Short description. Defaults to None.
            long_description (str | None, optional): Detailed description. Defaults to None.
            tlp (TLPType | None, optional): Traffic Light Protocol level. Defaults to None.
            user_tags (list[str] | None, optional): Tags with visibility prefixes. Defaults to None.
            permissions (list[PermissionType] | None, optional): Access permissions. Defaults to None.

        Returns:
            dict: Created saved search object.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-post
        """
        data: dict[str, Any] = _compact(
            {
                "datasource": datasource,
                "query": query,
                "name": name,
                "description": description,
                "longDescription": long_description,
                "tlp": tlp,
                "userTags": user_tags,
                "permissions": permissions,
            }
        )

        res = self.post("/api/v1/user/searches/", json=data)
        return self._response_to_json(res)

    def update(
        self,
        search_id: str,
        *,
        datasource: SavedSearchDataSource,
        query: str,
        name: str,
        description: str | None = None,
        long_description: str | None = None,
        tlp: TLPType | None = None,
        user_tags: list[str] | None = None,
        permissions: list[PermissionType] | None = None,
    ) -> dict:
        """Update an existing saved search.

        Args:
            search_id (str): ID of the saved search to update.
            datasource (SavedSearchDataSource): Data source to search ("hostnames" or "scans").
            query (str): Search API query string.
            name (str): User-facing name for the saved search.
            description (str | None, optional): Short description. Defaults to None.
            long_description (str | None, optional): Detailed description. Defaults to None.
            tlp (TLPType | None, optional): Traffic Light Protocol level. Defaults to None.
            user_tags (list[str] | None, optional): Tags with visibility prefixes. Defaults to None.
            permissions (list[PermissionType] | None, optional): Access permissions. Defaults to None.

        Returns:
            dict: Updated saved search object.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-put
        """
        data: dict[str, Any] = _compact(
            {
                "datasource": datasource,
                "query": query,
                "name": name,
                "description": description,
                "longDescription": long_description,
                "tlp": tlp,
                "userTags": user_tags,
                "permissions": permissions,
            }
        )

        res = self.put(f"/api/v1/user/searches/{search_id}/", json=data)
        return self._response_to_json(res)

    def remove(self, search_id: str) -> dict:
        """Delete a saved search.

        Args:
            search_id (str): ID of the saved search to delete.

        Returns:
            dict: Empty JSON object on success.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-delete
        """
        res = super().delete(f"/api/v1/user/searches/{search_id}/")
        return self._response_to_json(res)

    def get_results(self, search_id: str) -> dict:
        """Get results for a saved search.

        Args:
            search_id (str): ID of the saved search.

        Returns:
            dict: Search results matching the saved query.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-results
        """
        return self.get_json(f"/api/v1/user/searches/{search_id}/results/")
