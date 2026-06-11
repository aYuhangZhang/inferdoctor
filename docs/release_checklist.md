# v0.2.0 Release Checklist

## Product Experience

- [ ] `inferdoctor` shows the health dashboard without a subcommand.
- [ ] The dashboard includes all eight supported components.
- [ ] The heuristic score and status weights are visible and documented.
- [ ] Top fixes include a likely cause, next command, and config hint.
- [ ] Screenshot examples contain no private data.

## Diagnostics

- [ ] vLLM uses the reusable OpenAI-compatible checker.
- [ ] SGLang is available as `inferdoctor check sglang`.
- [ ] Connection refusal, timeout, 401/403, 404, invalid JSON, and wrong response shape are covered.
- [ ] Xinference and Dify behavior remains backward compatible.
- [ ] CPU-only machines complete without errors.

## Validation

- [ ] Run `python -m pip install -e ".[dev]"` in an isolated environment.
- [ ] Run `inferdoctor`.
- [ ] Run `inferdoctor check`.
- [ ] Run `inferdoctor check sglang`.
- [ ] Run `inferdoctor report --format markdown`.
- [ ] Run `pytest`.
- [ ] Run `git diff --check`.
- [ ] Confirm GitHub Actions passes on `dev`.

## Release

- [ ] Confirm package and module versions are `0.2.0`.
- [ ] Review README badges, examples, positioning, and roadmap.
- [ ] Review the final `dev` commit before merging to `main`.
- [ ] Create and push tag `v0.2.0` only after the release merge.
- [ ] Publish release notes with supported checks and safety limitations.
