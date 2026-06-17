# v0.2.0 Release Checklist

## Product Experience

- [x] `inferdoctor` shows the health dashboard without a subcommand.
- [x] The dashboard includes all eight supported components.
- [x] The heuristic score, stack summary, and status weights are visible and documented.
- [x] Top fixes include likely cause, impact, next command, and config hint.
- [x] Screenshot examples contain no private data.
- [x] README first screen explains the value and one-command quick start.

## Diagnostics

- [x] vLLM uses the reusable OpenAI-compatible checker.
- [x] SGLang is available as `inferdoctor check sglang`.
- [x] Connection refusal, timeout, 401/403, 404, invalid JSON, and wrong response shape are covered.
- [x] Xinference and Dify behavior remains backward compatible.
- [x] CPU-only machines complete without errors.
- [x] `inferdoctor explain <topic>` covers common local AI failures.
- [x] `inferdoctor capacity` provides a lightweight heuristic preview without running models.

## Validation

- [x] Run `python -m pip install -e ".[dev]"` in an isolated environment.
- [x] Run `inferdoctor`.
- [x] Run `inferdoctor check`.
- [x] Run `inferdoctor check sglang`.
- [x] Run `inferdoctor report --format markdown`.
- [x] Run `inferdoctor explain openai-compatible-404`.
- [x] Run `inferdoctor explain cuda-toolkit-missing`.
- [x] Run `inferdoctor capacity`.
- [x] Run `inferdoctor capacity --vram 24`.
- [x] Run `pytest`.
- [x] Run `git diff --check`.
- [ ] Confirm GitHub Actions passes on final `dev` commit.

## Release

- [x] Confirm package and module versions are `0.2.0`.
- [x] Review README badges, examples, positioning, and roadmap.
- [x] Review the final `dev` commit before merging to `main`.
- [ ] Open PR from `dev` to `main` for v0.2.0.
- [ ] Create and push tag `v0.2.0` only after the release merge.
- [ ] Publish release notes with supported checks and safety limitations.
