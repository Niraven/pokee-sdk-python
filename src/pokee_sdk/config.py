"""Client configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ClientConfig:
    """Configuration for the Pokee client.

    Attributes:
        api_key: Your Pokee API key. Defaults to the POKEE_API_KEY env var.
        base_url: Base URL for the Pokee API.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts for failed requests.
    """

    api_key: Optional[str] = field(default=None)
    base_url: str = "https://api.pokee.ai/v1"
    timeout: float = 30.0
    max_retries: int = 3

    def __post_init__(self) -> None:
        if self.api_key is None:
            object.__setattr__(self, "api_key", os.environ.get("POKEE_API_KEY"))
