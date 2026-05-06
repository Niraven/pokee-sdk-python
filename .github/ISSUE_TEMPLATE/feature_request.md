---
name: Feature Request
about: Suggest a new feature or improvement
title: "[Feature] "
labels: enhancement
assignees: ''
---

## Problem Statement

A clear description of the problem or limitation you're facing.

Example: "I need to batch multiple tasks together but there's no batch API..."

## Proposed Solution

Describe the API or behavior you'd like to see:

```python
# Example of how you'd like to use the feature
tasks = client.tasks.create_batch([
    {"skill": "gmail", "parameters": {...}},
    {"skill": "slack", "parameters": {...}},
])
```

## Alternatives Considered

Describe any alternative solutions or workarounds you've tried.

## Additional Context

- Is this blocking your use case?
- Are there other SDKs that handle this well? (link examples)
- Any relevant discussion or issues?
