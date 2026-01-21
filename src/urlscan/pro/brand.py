"""Brand API client module."""

from urlscan.client import BaseClient


class Brand(BaseClient):
    """Brand API client."""

    def get_available_brands(self) -> dict:
        """Get a list of brands that are tracked as part of urlscan's brand detection.

        Returns:
            dict: Response containing a list of brand objects.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/brands/availablebrands

        """
        return self.get_json("/api/v1/pro/availableBrands")

    def get_brands(self) -> dict:
        """Get a list of brands that we are able to detect phishing pages with the total number of detected pages and the latest hit for each brand.

        This is slower than the get_available method.

        Returns:
            dict: Response containing a list of brand object with detection statistics.

        Reference:
            https://docs.urlscan.io/apis/urlscan-openapi/brands/brandsummary

        """
        return self.get_json("/api/v1/pro/brands")
