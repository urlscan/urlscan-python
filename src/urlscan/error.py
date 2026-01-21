"""Exception classes for urlscan.io API errors."""


class URLScanError(Exception):
    """Base exception for urlscan.io API errors."""


class APIError(URLScanError):
    """Exception raised for API errors."""

    def __init__(self, message: str, *, status: int, description: str | None = None):
        """Initialize the API error.

        Args:
            message: Error message.
            status: HTTP status code.
            description: Optional error description.

        """
        self.message = message
        self.description = description
        self.status = status
        super().__init__(message)


class RateLimitError(APIError):
    """Exception raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        rate_limit_reset_after: float,
        description: str | None = None,
    ):
        """Initialize the rate limit error.

        Args:
            message: Error message.
            status: HTTP status code.
            rate_limit_reset_after: Seconds until rate limit resets.
            description: Optional error description.

        """
        super().__init__(message, description=description, status=status)
        self.rate_limit_reset_after = rate_limit_reset_after


class RateLimitRemainingError(URLScanError):
    """Exception raised when rate limit remaining is zero."""
