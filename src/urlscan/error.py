class URLScanError(Exception):
    pass


class APIError(URLScanError):
    def __init__(self, message: str, *, status: int, description: str | None = None):
        self.message = message
        self.description = description
        self.status = status
        super().__init__(message)


class RateLimitError(APIError):
    def __init__(
        self,
        message: str,
        *,
        status: int,
        rate_limit_reset_after: float,
        description: str | None = None,
    ):
        super().__init__(message, description=description, status=status)
        self.rate_limit_reset_after = rate_limit_reset_after


class RateLimitRemainingError(URLScanError):
    pass
