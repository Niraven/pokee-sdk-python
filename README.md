# Pokee Python SDK

> Public-safe notice: this repository is an independent/experimental client wrapper and portfolio artifact. It is not an official Pokee AI release unless Pokee explicitly adopts and republishes it. It contains no private Pokee source code, credentials, customer data, internal documentation, or non-public implementation details.

Python client patterns for working with a Pokee-style task API: task creation, task lookup, cancellation, pagination, typed errors, and async usage.

## Installation

```bash
pip install pokee-sdk
```

Or with Poetry:

```bash
poetry add pokee-sdk
```

Install from source:

```bash
git clone https://github.com/Niraven/pokee-sdk-python.git
cd pokee-sdk-python
pip install -e ".[dev]"
```

## Quick Start

```python
from pokee_sdk import Pokee

client = Pokee(api_key="pk_test_or_your_own_key")

task = client.tasks.create(
    skill="gmail",
    parameters={
        "to": "team@example.com",
        "subject": "Weekly Report",
        "body": "...",
    },
)

print(f"Task {task.id} status: {task.status}")
```

## Authentication

Pass an API key directly or set the `POKEE_API_KEY` environment variable:

```bash
export POKEE_API_KEY="your_key_here"
```

```python
from pokee_sdk import Pokee

client = Pokee()
```

Never commit real keys, OAuth tokens, workspace IDs, customer data, or logs.

## Usage

### Creating Tasks

```python
from pokee_sdk import Pokee

client = Pokee()

task = client.tasks.create(
    skill="slack",
    parameters={
        "channel": "#engineering",
        "message": "Deployment complete",
    },
)
```

### Listing & Filtering Tasks

```python
from pokee_sdk import TaskStatus

running = client.tasks.list(status=TaskStatus.RUNNING)
gmail_tasks = client.tasks.list(skill="gmail", per_page=50)
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

productivity = client.skills.list(category="productivity")
```

## Async Support

```python
import asyncio
from pokee_sdk import AsyncPokee

async def main():
    async with AsyncPokee() as client:
        task = await client.tasks.create(
            skill="google_sheets",
            parameters={"spreadsheet_id": "sheet_id", "range": "A1:D10"},
        )
        print(task.result)

asyncio.run(main())
```

## Error Handling

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
    print("Check your API key")
except NotFoundError:
    print("Task not found")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except ValidationError as e:
    print(f"Invalid request: {e}")
except APIConnectionError:
    print("Could not connect to the API")
```

## Configuration

```python
client = Pokee(
    api_key="your_key_here",
    base_url="https://api.pokee.ai/v1",
    timeout=60.0,
    max_retries=5,
)
```

## Public-Safe Scope

This repo should stay limited to:

- generic SDK/client patterns
- public endpoint shapes
- placeholder examples
- typed models and exceptions
- tests with mocked responses only

Do not add:

- private product strategy
- unreleased feature details
- internal docs or screenshots
- customer workflows, files, logs, or identifiers
- real API keys, OAuth tokens, cookies, or workspace IDs

## License

MIT. Pokee AI trademarks and product names belong to their respective owner.
