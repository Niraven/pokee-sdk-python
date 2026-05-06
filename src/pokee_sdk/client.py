"""Pokee API client implementations."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import httpx

from pokee_sdk.config import ClientConfig
from pokee_sdk.exceptions import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)
from pokee_sdk.models import Skill, SkillList, Task, TaskList, TaskStatus


class Pokee:
    """Synchronous client for the Pokee AI API.

    Usage:
        client = Pokee(api_key="pk_live_...")
        task = client.tasks.create(skill="gmail", parameters={...})
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ) -> None:
        config_kwargs: Dict[str, Any] = {}
        if api_key is not None:
            config_kwargs["api_key"] = api_key
        if base_url is not None:
            config_kwargs["base_url"] = base_url
        if timeout is not None:
            config_kwargs["timeout"] = timeout
        if max_retries is not None:
            config_kwargs["max_retries"] = max_retries

        self._config = ClientConfig(**config_kwargs)

        if not self._config.api_key:
            raise AuthenticationError(
                "API key is required. Pass api_key or set the POKEE_API_KEY environment variable."
            )

        self._client = httpx.Client(
            base_url=self._config.base_url,
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "pokee-sdk-python/0.1.0",
            },
            timeout=self._config.timeout,
        )
        self.tasks = _TasksResource(self)
        self.skills = _SkillsResource(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        last_error: Optional[Exception] = None

        for attempt in range(self._config.max_retries + 1):
            try:
                response = self._client.request(method, path, json=json, params=params)
                return self._handle_response(response)
            except httpx.ConnectError as e:
                last_error = APIConnectionError(f"Connection failed: {e}")
            except RateLimitError as e:
                last_error = e
                if attempt < self._config.max_retries:
                    wait = e.retry_after or (2**attempt)
                    time.sleep(wait)
                    continue
                raise
            except APIError:
                raise
            except httpx.HTTPError as e:
                last_error = APIConnectionError(f"Request failed: {e}")

            if attempt < self._config.max_retries:
                time.sleep(2**attempt)

        raise last_error or APIConnectionError("Request failed after retries")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        request_id = response.headers.get("x-request-id")

        if response.status_code == 401:
            raise AuthenticationError(
                "Invalid API key", status_code=401, request_id=request_id
            )
        if response.status_code == 404:
            raise NotFoundError(
                "Resource not found", status_code=404, request_id=request_id
            )
        if response.status_code == 422:
            data = response.json()
            raise ValidationError(
                data.get("message", "Validation failed"),
                status_code=422,
                request_id=request_id,
            )
        if response.status_code == 429:
            retry_after = response.headers.get("retry-after")
            raise RateLimitError(
                retry_after=float(retry_after) if retry_after else None,
                status_code=429,
                request_id=request_id,
            )
        if response.status_code >= 400:
            try:
                data = response.json()
                msg = data.get("message", response.text)
            except Exception:
                msg = response.text
            raise APIError(msg, status_code=response.status_code, request_id=request_id)

        return response.json()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "Pokee":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()


class AsyncPokee:
    """Asynchronous client for the Pokee AI API.

    Usage:
        async with AsyncPokee(api_key="pk_live_...") as client:
            task = await client.tasks.create(skill="gmail", parameters={...})
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ) -> None:
        config_kwargs: Dict[str, Any] = {}
        if api_key is not None:
            config_kwargs["api_key"] = api_key
        if base_url is not None:
            config_kwargs["base_url"] = base_url
        if timeout is not None:
            config_kwargs["timeout"] = timeout
        if max_retries is not None:
            config_kwargs["max_retries"] = max_retries

        self._config = ClientConfig(**config_kwargs)

        if not self._config.api_key:
            raise AuthenticationError(
                "API key is required. Pass api_key or set the POKEE_API_KEY environment variable."
            )

        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            headers={
                "Authorization": f"Bearer {self._config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "pokee-sdk-python/0.1.0",
            },
            timeout=self._config.timeout,
        )
        self.tasks = _AsyncTasksResource(self)
        self.skills = _AsyncSkillsResource(self)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        import asyncio

        last_error: Optional[Exception] = None

        for attempt in range(self._config.max_retries + 1):
            try:
                response = await self._client.request(method, path, json=json, params=params)
                return self._handle_response(response)
            except httpx.ConnectError as e:
                last_error = APIConnectionError(f"Connection failed: {e}")
            except RateLimitError as e:
                last_error = e
                if attempt < self._config.max_retries:
                    wait = e.retry_after or (2**attempt)
                    await asyncio.sleep(wait)
                    continue
                raise
            except APIError:
                raise
            except httpx.HTTPError as e:
                last_error = APIConnectionError(f"Request failed: {e}")

            if attempt < self._config.max_retries:
                await asyncio.sleep(2**attempt)

        raise last_error or APIConnectionError("Request failed after retries")

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        request_id = response.headers.get("x-request-id")

        if response.status_code == 401:
            raise AuthenticationError(
                "Invalid API key", status_code=401, request_id=request_id
            )
        if response.status_code == 404:
            raise NotFoundError(
                "Resource not found", status_code=404, request_id=request_id
            )
        if response.status_code == 422:
            data = response.json()
            raise ValidationError(
                data.get("message", "Validation failed"),
                status_code=422,
                request_id=request_id,
            )
        if response.status_code == 429:
            retry_after = response.headers.get("retry-after")
            raise RateLimitError(
                retry_after=float(retry_after) if retry_after else None,
                status_code=429,
                request_id=request_id,
            )
        if response.status_code >= 400:
            try:
                data = response.json()
                msg = data.get("message", response.text)
            except Exception:
                msg = response.text
            raise APIError(msg, status_code=response.status_code, request_id=request_id)

        return response.json()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncPokee":
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()


class _TasksResource:
    def __init__(self, client: Pokee) -> None:
        self._client = client

    def create(
        self,
        *,
        skill: str,
        parameters: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """Create and execute a new task."""
        body: Dict[str, Any] = {"skill": skill}
        if parameters:
            body["parameters"] = parameters
        if name:
            body["name"] = name
        if metadata:
            body["metadata"] = metadata
        data = self._client._request("POST", "/tasks", json=body)
        return Task(**data)

    def get(self, task_id: str) -> Task:
        """Retrieve a task by ID."""
        data = self._client._request("GET", f"/tasks/{task_id}")
        return Task(**data)

    def list(
        self,
        *,
        status: Optional[TaskStatus] = None,
        skill: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> TaskList:
        """List tasks with optional filtering."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status.value if isinstance(status, TaskStatus) else status
        if skill:
            params["skill"] = skill
        data = self._client._request("GET", "/tasks", params=params)
        return TaskList(**data)

    def cancel(self, task_id: str) -> Task:
        """Cancel a running task."""
        data = self._client._request("POST", f"/tasks/{task_id}/cancel")
        return Task(**data)


class _AsyncTasksResource:
    def __init__(self, client: AsyncPokee) -> None:
        self._client = client

    async def create(
        self,
        *,
        skill: str,
        parameters: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        """Create and execute a new task."""
        body: Dict[str, Any] = {"skill": skill}
        if parameters:
            body["parameters"] = parameters
        if name:
            body["name"] = name
        if metadata:
            body["metadata"] = metadata
        data = await self._client._request("POST", "/tasks", json=body)
        return Task(**data)

    async def get(self, task_id: str) -> Task:
        """Retrieve a task by ID."""
        data = await self._client._request("GET", f"/tasks/{task_id}")
        return Task(**data)

    async def list(
        self,
        *,
        status: Optional[TaskStatus] = None,
        skill: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> TaskList:
        """List tasks with optional filtering."""
        params: Dict[str, Any] = {"page": page, "per_page": per_page}
        if status:
            params["status"] = status.value if isinstance(status, TaskStatus) else status
        if skill:
            params["skill"] = skill
        data = await self._client._request("GET", "/tasks", params=params)
        return TaskList(**data)

    async def cancel(self, task_id: str) -> Task:
        """Cancel a running task."""
        data = await self._client._request("POST", f"/tasks/{task_id}/cancel")
        return Task(**data)


class _SkillsResource:
    def __init__(self, client: Pokee) -> None:
        self._client = client

    def list(self, *, category: Optional[str] = None) -> SkillList:
        """List available skills."""
        params: Dict[str, Any] = {}
        if category:
            params["category"] = category
        data = self._client._request("GET", "/skills", params=params)
        return SkillList(**data)

    def get(self, skill_id: str) -> Skill:
        """Get details for a specific skill."""
        data = self._client._request("GET", f"/skills/{skill_id}")
        return Skill(**data)


class _AsyncSkillsResource:
    def __init__(self, client: AsyncPokee) -> None:
        self._client = client

    async def list(self, *, category: Optional[str] = None) -> SkillList:
        """List available skills."""
        params: Dict[str, Any] = {}
        if category:
            params["category"] = category
        data = await self._client._request("GET", "/skills", params=params)
        return SkillList(**data)

    async def get(self, skill_id: str) -> Skill:
        """Get details for a specific skill."""
        data = await self._client._request("GET", f"/skills/{skill_id}")
        return Skill(**data)
