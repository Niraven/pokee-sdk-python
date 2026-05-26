"""Tests for the Pokee client."""

from __future__ import annotations

import os
from unittest.mock import patch

import httpx
import pytest
import respx

from pokee_sdk import AsyncPokee, Pokee, Task, TaskStatus
from pokee_sdk.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)


@pytest.fixture
def api_key() -> str:
    return "pk_test_abc123"


@pytest.fixture
def client(api_key: str) -> Pokee:
    return Pokee(api_key=api_key, base_url="https://api.pokee.ai/v1")


class TestClientInit:
    def test_requires_api_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("POKEE_API_KEY", None)
            with pytest.raises(AuthenticationError, match="API key is required"):
                Pokee()

    def test_accepts_api_key_param(self, api_key: str) -> None:
        client = Pokee(api_key=api_key)
        assert client._config.api_key == api_key

    def test_reads_env_var(self) -> None:
        with patch.dict(os.environ, {"POKEE_API_KEY": "pk_test_env"}):
            client = Pokee()
            assert client._config.api_key == "pk_test_env"

    def test_custom_base_url(self, api_key: str) -> None:
        client = Pokee(api_key=api_key, base_url="https://custom.api.com")
        assert client._config.base_url == "https://custom.api.com"

    def test_context_manager(self, api_key: str) -> None:
        with Pokee(api_key=api_key) as client:
            assert client._config.api_key == api_key


class TestTasks:
    @respx.mock
    def test_create_task(self, client: Pokee) -> None:
        respx.post("https://api.pokee.ai/v1/tasks").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "task_001",
                    "name": "Send email",
                    "status": "pending",
                    "skill": "gmail",
                    "parameters": {"to": "user@example.com"},
                    "created_at": "2024-01-01T00:00:00Z",
                },
            )
        )

        task = client.tasks.create(
            skill="gmail",
            parameters={"to": "user@example.com"},
            name="Send email",
        )

        assert isinstance(task, Task)
        assert task.id == "task_001"
        assert task.status == TaskStatus.PENDING
        assert task.skill == "gmail"

    @respx.mock
    def test_get_task(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/task_001").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "task_001",
                    "name": "Send email",
                    "status": "completed",
                    "skill": "gmail",
                    "parameters": {},
                    "result": {"message_id": "msg_123"},
                    "created_at": "2024-01-01T00:00:00Z",
                    "completed_at": "2024-01-01T00:00:05Z",
                },
            )
        )

        task = client.tasks.get("task_001")
        assert task.status == TaskStatus.COMPLETED
        assert task.result == {"message_id": "msg_123"}

    @respx.mock
    def test_list_tasks(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks").mock(
            return_value=httpx.Response(
                200,
                json={
                    "tasks": [
                        {
                            "id": "task_001",
                            "name": "Task 1",
                            "status": "completed",
                            "skill": "gmail",
                            "parameters": {},
                            "created_at": "2024-01-01T00:00:00Z",
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 20,
                    "has_more": False,
                },
            )
        )

        result = client.tasks.list()
        assert result.total == 1
        assert len(result.tasks) == 1


class TestErrorHandling:
    @respx.mock
    def test_authentication_error(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/x").mock(
            return_value=httpx.Response(401, json={"message": "Unauthorized"})
        )

        with pytest.raises(AuthenticationError):
            client.tasks.get("x")

    @respx.mock
    def test_not_found_error(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/missing").mock(
            return_value=httpx.Response(404, json={"message": "Not found"})
        )

        with pytest.raises(NotFoundError):
            client.tasks.get("missing")

    @respx.mock
    def test_rate_limit_error(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/x").mock(
            return_value=httpx.Response(
                429,
                json={"message": "Rate limited"},
                headers={"retry-after": "5"},
            )
        )

        with pytest.raises(RateLimitError) as exc_info:
            client.tasks.get("x")
        assert exc_info.value.retry_after == 5.0

    @respx.mock
    def test_validation_error_with_plain_text_body(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/invalid").mock(
            return_value=httpx.Response(422, text="invalid task id")
        )

        with pytest.raises(ValidationError, match="invalid task id"):
            client.tasks.get("invalid")

    @respx.mock
    def test_api_error_with_plain_text_body(self, client: Pokee) -> None:
        respx.get("https://api.pokee.ai/v1/tasks/x").mock(
            return_value=httpx.Response(500, text="upstream unavailable")
        )

        with pytest.raises(APIError, match="upstream unavailable"):
            client.tasks.get("x")


@pytest.mark.asyncio
class TestAsyncClient:
    @respx.mock
    async def test_create_task(self) -> None:
        respx.post("https://api.pokee.ai/v1/tasks").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": "task_002",
                    "name": "Async task",
                    "status": "running",
                    "skill": "slack",
                    "parameters": {},
                    "created_at": "2024-01-01T00:00:00Z",
                },
            )
        )

        async with AsyncPokee(api_key="pk_test_abc") as client:
            task = await client.tasks.create(skill="slack", parameters={})
            assert task.id == "task_002"
            assert task.status == TaskStatus.RUNNING
