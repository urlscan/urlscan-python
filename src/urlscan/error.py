"""Exception classes for urlscan.io API errors."""


class URLScanError(Exception):
    """Base exception for urlscan.io API errors."""


class ItemError(URLScanError):
    """Error item."""

    def __init__(
        self,
        title: str,
        status: int,
        code: str | None = None,
        description: str | None = None,
        detail: str | None = None,
    ):
        """Initialize the error item.

        Args:
            title (str): error title.
            status (int): error status.
            code (str | None, optional): error code. Defaults to None.
            description (str | None, optional): error description. Defaults to None.
            detail (str | None, optional): error detail. Defaults to None.

        """
        self.title = title
        self.status = status
        self.code = code
        self.description = description
        self.detail = detail

        super().__init__(title)


class APIError(URLScanError):
    """Exception raised for API errors."""

    def __init__(
        self,
        message: str,
        *,
        status: int,
        description: str | None = None,
        errors: list[ItemError] | None = None,
        code: str | None = None,
        type_: str | None = None,
    ):
        """Initialize the API error.

        Args:
            message (str): error message.
            status (int): error status.
            description (str | None, optional): error description. Defaults to None.
            errors (list[ErrorItem] | None, optional): error items. Defaults to None.
            code (str | None, optional): error code. Defaults to None.
            type_ (str | None, optional): error type. Defaults to None.

        """
        self.message = message
        self.description = description
        self.status = status
        self.errors = errors
        self.code = code
        self.type = type_
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
