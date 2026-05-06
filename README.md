# Pokee Python SDK

[![PyPI version](https://img.shields.io/pypi/v/pokee-sdk.svg)](https://pypi.org/project/pokee-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/pokee-sdk.svg)](https://pypi.org/project/pokee-sdk/)
[![CI](https://github.com/Niraven/pokee-sdk-python/actions/workflows/test.yml/badge.svg)](https://github.com/Niraven/pokee-sdk-python/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python client library for the [Pokee AI](https://pokee.ai) platform. Automate workflows across 90+ integrations — Gmail, Slack, GitHub, Google Sheets, and more — with a simple, type-safe API.

## Installation

```bash
pip install pokee-sdk
```

Or with [Poetry](https://python-poetry.org/):

```bash
poetry add pokee-sdk
```

<details>
<summary>Install from source</summary>

```bash
git clone https://github.com/Niraven/pokee-sdk-python.git
cd pokee-sdk-python
pip install -e ".[dev]"
```

</details>

## Quick Start

```python
from pokee_sdk import Pokee

client = Pokee(api_key="pk_live_...")

task = client.tasks.create(
    skill="gmail",
    parameters={"to": "team@company.com", "subject": "Weekly Report", "body": "..."}
)

print(f"Task {task.id} status: {task.status}")
```

## Authentication

Get your API key from the [Pokee Dashboard](https://app.pokee.ai/settings/api-keys).

You can pass it directly or set the `POKEE_API_KEY` environment variable:

```bash
export POKEE_API_KEY="pk_live_..."
```

```python
from pokee_sdk import Pokee

# Reads from POKEE_API_KEY automatically
client = Pokee()
```

## Usage

### Creating Tasks

Tasks are the core primitive — each task executes a skill with given parameters:

```python
from pokee_sdk import Pokee

client = Pokee()

# Send a Slack message
task = client.tasks.create(
    skill="slack",
    parameters={
        "channel": "#engineering",
        "message": "Deployment complete! :rocket:"
    }
)
```

### Listing & Filtering Tasks

```python
from pokee_sdk import TaskStatus

# Get all running tasks
running = client.tasks.list(status=TaskStatus.RUNNING)

# Filter by skill
gmail_tasks = client.tasks.list(skill="gmail", per_page=50)

# Paginate
page2 = client.tasks.list(page=2)
```

### Retrieving a Task

```python
task = client.tasks.get("task_abc123")

if task.status == "completed":
    print(task.result)
elif task.error:
    print(f"Failed: {task.error}")
```

### Cancelling a Task

```python
cancelled = client.tasks.cancel("task_abc123")
```

### Listing Available Skills

```python
skills = client.skills.list()
for skill in skills.skills:
    print(f"{skill.name}: {skill.description}")

# Filter by category
productivity = client.skills.list(category="productivity")
```

## Async Support

The SDK includes a fully async client for use with `asyncio`:

```python
import asyncio
from pokee_sdk import AsyncPokee

async def main():
    async with AsyncPokee() as client:
        task = await client.tasks.create(
            skill="google_sheets",
            parameters={"spreadsheet_id": "...", "range": "A1:D10"}
        )
        print(task.result)

asyncio.run(main())
```

## Error Handling

The SDK raises typed exceptions for different error scenarios:

```python
from pokee_sdk import Pokee
from pokee_sdk.exceptions import (
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
    APIConnectionError,
)

client = Pokee()

try:
    task = client.tasks.get("task_nonexistent")
except AuthenticationError:
    # Invalid or expired API key
    print("Check your API key")
except NotFoundError:
    # Task doesn't exist
    print("Task not found")
except RateLimitError as e:
    # Too many requests — retry after the given duration
    print(f"Rate limited. Retry after {e.retry_after}s")
except ValidationError as e:
    # Invalid parameters
    print(f"Invalid request: {e}")
except APIConnectionError:
    # Network issues
    print("Could not connect to Pokee API")
```

## Configuration

```python
client = Pokee(
    api_key="pk_live_...",
    base_url="https://api.pokee.ai/v1",  # Custom endpoint
    timeout=60.0,                          # Request timeout (seconds)
    max_retries=5,                         # Retry attempts for transient errors
)
```

## Advanced Usage

### Using as a Context Manager

```python
with Pokee() as client:
    task = client.tasks.create(skill="gmail", parameters={...})
# Client is automatically closed
```

### Task Metadata

Attach custom metadata to tasks for tracking:

```python
task = client.tasks.create(
    skill="slack",
    parameters={"channel": "#alerts", "message": "Server down"},
    name="Alert: Production Issue",
    metadata={"severity": "high", "triggered_by": "monitoring"}
)
```

### Polling for Completion

```python
import time

task = client.tasks.create(skill="gmail", parameters={...})

while task.status in ("pending", "running"):
    time.sleep(2)
    task = client.tasks.get(task.id)

if task.status == "completed":
    print("Done!", task.result)
else:
    print("Failed:", task.error)
```

## API Reference

### Client Classes

| Class | Description |
|-------|-------------|
| `Pokee` | Synchronous client |
| `AsyncPokee` | Asynchronous client for asyncio |

### Resources

| Resource | Methods |
|----------|---------|
| `client.tasks` | `create()`, `get()`, `list()`, `cancel()` |
| `client.skills` | `list()`, `get()` |

### Models

| Model | Description |
|-------|-------------|
| `Task` | A task execution with status, result, and metadata |
| `TaskList` | Paginated list of tasks |
| `TaskStatus` | Enum: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED` |
| `Skill` | Available skill with schema information |

### Exceptions

| Exception | HTTP Status | Description |
|-----------|-------------|-------------|
| `APIError` | Various | Base class for all API errors |
| `AuthenticationError` | 401 | Invalid or missing API key |
| `NotFoundError` | 404 | Resource not found |
| `ValidationError` | 422 | Invalid request parameters |
| `RateLimitError` | 429 | Rate limit exceeded |
| `APIConnectionError` | — | Network connectivity issues |

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
