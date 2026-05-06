# Contributing to Pokee Python SDK

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Niraven/pokee-sdk-python.git
   cd pokee-sdk-python
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

## Running Tests

```bash
pytest
pytest --cov=pokee_sdk       # with coverage
pytest tests/test_client.py   # specific file
```

## Code Quality

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
ruff check .          # lint
ruff format .         # format
mypy src/             # type checking
```

## Pull Request Process

1. **Fork** the repository and create a feature branch from `main`.
2. **Write tests** for any new functionality.
3. **Ensure all checks pass** — run `pytest`, `ruff check`, and `mypy` locally.
4. **Write a clear PR description** explaining what changed and why.
5. **Keep commits focused** — one logical change per commit.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add webhook support to tasks resource
fix: handle timeout in async client retry loop
docs: update authentication examples in README
test: add coverage for rate limit backoff
```

## Code Style

- All public APIs must have type annotations.
- Keep functions focused and small.
- Use descriptive variable names.
- Avoid abbreviations in public interfaces.

## Reporting Bugs

Use the [bug report template](https://github.com/Niraven/pokee-sdk-python/issues/new?template=bug_report.md) and include:

- Python version and OS
- SDK version (`pokee_sdk.__version__`)
- Minimal reproduction steps
- Expected vs. actual behavior

## Feature Requests

Open an issue using the [feature request template](https://github.com/Niraven/pokee-sdk-python/issues/new?template=feature_request.md). Describe the use case and proposed API surface.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
