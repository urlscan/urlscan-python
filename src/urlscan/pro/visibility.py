"""Visibility API client module."""

from urlscan.client import BaseClient
from urlscan.types import UpdateVisibilityType


class Visibility(BaseClient):
    """Visibility API client."""

    def update(self, uuid: str, visibility: UpdateVisibilityType) -> dict:
        """Update visibility of a scan owned by you or your team.

        Args:
            uuid (str): The UUID of a scan.
            visibility (UpdateVisibilityType):  The new visibility of the scan result: public, unlisted, private, deleted

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/scanning/updateresultvisibility

        """
        if visibility not in ["public", "private", "unlisted", "deleted"]:
            raise ValueError(
                "Visibility must be either 'public', 'private', 'unlisted', or 'deleted'"
            )

        res = self._put(
            f"/api/v1/result/{uuid}/visibility/",
            json={"visibility": visibility},
        )
        return self._response_to_json(res)

    def reset(self, uuid: str) -> dict:
        """Reset the visibility of a scan owned by you or your team to its original visibility.

        Args:
            uuid (str): The UUID of a scan.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/scanning/deleteresultvisibility

        """
        res = self._delete(f"/api/v1/result/{uuid}/visibility/")
        return self._response_to_json(res)
