# Contributing to InferDoctor

Thank you for helping improve lightweight diagnostics for local AI inference
stacks.

## Before You Start

- Search existing issues before opening a new one.
- Keep changes focused on diagnostics, reporting, documentation, or tests.
- Do not add AI runtimes, GPU frameworks, model downloads, or destructive
  system-management behavior.
- Preserve read-only behavior unless a future proposal explicitly documents and
  isolates an opt-in action.

## Development Setup

```bash
git clone git@github.com:anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e ".[dev]"
pytest
```

The test suite must run without a GPU, CUDA, internet access, or local inference
services. Mock subprocess and HTTP behavior instead of depending on a developer
machine's configuration.

## Adding a Checker

1. Implement the `Checker` interface in `inferdoctor/checkers/`.
2. Return a `CheckResult` with `name`, `status`, `summary`, `details`,
   `suggestions`, and `raw_data`.
3. Register the checker in `inferdoctor/checkers/__init__.py`.
4. Handle missing commands, refused connections, malformed output, and timeouts.
5. Add mock-based tests and document the new check.

Use `skip` for absent optional components, `warn` for incomplete or suspicious
setups, and `fail` for discovered components that are broken or checker errors.

## Pull Requests

- Explain the problem and why the change is appropriately scoped.
- Include tests for behavior changes.
- Run `pytest` and `git diff --check`.
- Update user-facing documentation when CLI or report behavior changes.
- Avoid unrelated formatting or refactoring.

Contributions are accepted under the repository's Apache License 2.0.
