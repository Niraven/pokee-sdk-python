# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-12-01

### Added

- Initial release of the Pokee Python SDK.
- Synchronous client (`Pokee`) and async client (`AsyncPokee`).
- Tasks resource: `create`, `get`, `list`, `cancel`.
- Skills resource: `list`, `get`.
- Typed exception hierarchy: `APIError`, `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ValidationError`, `APIConnectionError`.
- Automatic retry with exponential backoff for transient failures.
- Pydantic models for all API responses.
- Full type annotations and `py.typed` marker.
- Comprehensive test suite with `pytest` and `respx`.

[Unreleased]: https://github.com/Niraven/pokee-sdk-python/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Niraven/pokee-sdk-python/releases/tag/v0.1.0
