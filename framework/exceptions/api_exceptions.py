class APIClientError(Exception):
    """Base exception for API client errors."""


class APIConnectionError(APIClientError):
    """Raised when the API server cannot be reached."""


class APITimeoutError(APIClientError):
    """Raised when an API request times out."""
