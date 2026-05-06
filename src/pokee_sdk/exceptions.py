"""Exception types for the Pokee SDK."""

from __future__ import annotations

from typing import Optional


class APIError(Exception):
    """Base exception for all Pokee API errors."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(message)


class AuthenticationError(APIError):
    """Raised when API key is invalid or missing."""

    pass


class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        *,
        retry_after: Optional[float] = None,
        **kwargs: object,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, **kwargs)  # type: ignore[arg-type]


class NotFoundError(APIError):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(APIError):
    """Raised when request validation fails."""

    pass


class APIConnectionError(APIError):
    """Raised when the client cannot connect to the API."""

    pass
