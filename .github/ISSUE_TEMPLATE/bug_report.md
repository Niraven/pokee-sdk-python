---
name: Bug Report
about: Report a bug to help us improve
title: "[Bug] "
labels: bug
assignees: ''
---

## Describe the Bug

A clear and concise description of what the bug is.

## To Reproduce

Steps to reproduce the behavior:

1. Initialize client with `Pokee(...)`
2. Call `client.tasks.create(...)`
3. See error

## Expected Behavior

A clear description of what you expected to happen.

## Actual Behavior

What actually happened, including any error messages or stack traces.

## Environment

- **OS:** [e.g., macOS 14.0, Ubuntu 22.04]
- **Python version:** [e.g., 3.11.5]
- **SDK version:** [e.g., 0.1.0]

## Code Sample

```python
# Minimal reproduction
from pokee_sdk import Pokee

client = Pokee(api_key="...")
# ...
```

## Additional Context

Add any other context about the problem here (logs, screenshots, etc.).
