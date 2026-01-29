"""Saved search API client module."""

from typing import Any

from urlscan.client import BaseClient, _compact
from urlscan.types import PermissionType, SavedSearchDataSource, TLPType


class SavedSearch(BaseClient):
    """Saved Search API client."""

    def get_list(self) -> dict:
        """Get a list of Saved Searches for the current user.

        Returns:
            dict: Response containing an array of Saved Search objects with their properties.

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
        """Create a Saved Search.

        Args:
            datasource (SavedSearchDataSource): Which data this Saved Search operates on
                ("hostnames" or "scans").
            query (str): Search API query string.
            name (str): User-facing short name for the saved search.
            description (str | None, optional): Short description. Defaults to None.
            long_description (str | None, optional): Long description. Defaults to None.
            tlp (TLPType | None, optional): TLP (Traffic Light Protocol) indicator for
                other users on the urlscan Pro platform. Valid values: "red", "amber+strict",
                "amber", "green", "clear". Defaults to None.
            user_tags (list[str] | None, optional): User-supplied tags to be applied to
                matching items. Apply the following prefixes to tags to define their
                visibility scope: `pro.` (urlscan Pro users), `public.` (all registered
                users), `private.` (only you), or `team.` (you and team members).
                Defaults to None.
            permissions (list[PermissionType] | None, optional): Determine whether only
                other users on the same team or everyone on urlscan Pro can see the search.
                Valid values: "public:read", "team:read", "team:write". Defaults to None.

        Returns:
            dict: Created Saved Search object containing the search properties and unique _id.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-post

        """
        search: dict[str, Any] = _compact(
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
        data: dict[str, Any] = {"search": search}

        res = self._post("/api/v1/user/searches/", json=data)
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
        """Update a Saved Search.

        Args:
            search_id (str): Unique ID of the saved search to update.
            datasource (SavedSearchDataSource): Which data this Saved Search operates on
                ("hostnames" or "scans").
            query (str): Search API query string.
            name (str): User-facing short name for the saved search.
            description (str | None, optional): Short description. Defaults to None.
            long_description (str | None, optional): Long description. Defaults to None.
            tlp (TLPType | None, optional): TLP (Traffic Light Protocol) indicator for
                other users on the urlscan Pro platform. Valid values: "red", "amber+strict",
                "amber", "green", "clear". Defaults to None.
            user_tags (list[str] | None, optional): User-supplied tags to be applied to
                matching items. Apply the following prefixes to tags to define their
                visibility scope: `pro.` (urlscan Pro users), `public.` (all registered
                users), `private.` (only you), or `team.` (you and team members).
                Defaults to None.
            permissions (list[PermissionType] | None, optional): Determine whether only
                other users on the same team or everyone on urlscan Pro can see the search.
                Valid values: "public:read", "team:read", "team:write". Defaults to None.

        Returns:
            dict: Updated Saved Search object containing the search properties and unique _id.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-put

        """
        search: dict[str, Any] = _compact(
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
        data: dict[str, Any] = {"search": search}

        res = self._put(f"/api/v1/user/searches/{search_id}/", json=data)
        return self._response_to_json(res)

    def remove(self, search_id: str) -> dict:
        """Delete a Saved Search.

        Args:
            search_id (str): Unique ID of the saved search to delete.

        Returns:
            dict: Empty JSON object on success.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-delete

        """
        res = super()._delete(f"/api/v1/user/searches/{search_id}/")
        return self._response_to_json(res)

    def get_results(self, search_id: str) -> dict:
        """Get the search results for a specific Saved Search.

        Args:
            search_id (str): Unique ID of the saved search.

        Returns:
            dict: Search results matching the saved query. The structure depends on the
                datasource (hostnames or scans) specified in the saved search.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/saved-searches/savedsearches-results

        """
        return self.get_json(f"/api/v1/user/searches/{search_id}/results/")
