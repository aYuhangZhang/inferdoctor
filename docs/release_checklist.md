# v0.4.0 Release Checklist

This checklist is public-facing release preparation for InferDoctor v0.4.0. It should stay free of private workflow notes, transcripts, and internal planning artifacts.

## Product Experience

- [x] `inferdoctor` shows the local AI stack health dashboard without a subcommand.
- [x] `inferdoctor recommend` explains a practical setup direction for common goals.
- [x] `inferdoctor stack plan` gives beginner-friendly next actions.
- [x] `inferdoctor template list` and `inferdoctor template show` explain available starter projects.
- [x] `inferdoctor template create` generates customer service, restaurant ordering, and local document Q&A starters.
- [x] `inferdoctor template validate` checks generated projects without running inference.
- [x] `inferdoctor init` supports a guided setup path.
- [x] `inferdoctor model fit` gives clearly labeled heuristic fit guidance.

## Safety

- [x] No heavy AI runtime dependencies were added.
- [x] No model download command was added.
- [x] No model execution command was added.
- [x] No automatic runtime installation was added.
- [x] Diagnostics remain read-only by default.
- [x] Template generation writes only to an explicit output directory.
- [x] Recommendations and model-fit estimates are documented as heuristics, not benchmarks.

## Validation

- [x] CLI smoke test: `inferdoctor`.
- [x] CLI help smoke test: key command groups render help cleanly.
- [x] Generated template smoke test: create customer service, restaurant ordering, and local document Q&A starters.
- [x] Template validation smoke test: validate generated starter projects.
- [x] Wheel build smoke test: `python -m build`.
- [x] Package metadata check: `twine check dist/*`.
- [x] Clean wheel install smoke test in a temporary virtual environment.
- [x] Unit tests: `pytest`.
- [x] Documentation review for install wording, safety claims, and beginner flow.
- [x] README install wording does not claim PyPI availability before publication.
- [x] Public release notes draft exists for v0.4.0.
- [x] Internal artifact scan is part of pre-commit/final validation.

## Release Preparation

- [x] Confirm package and module versions are `0.4.0` on the release branch.
- [ ] Confirm GitHub Actions passes on the final `dev` commit.
- [ ] Review final diff before merging `dev` to `main`.
- [ ] Merge `dev` to `main` only when v0.4.0 is approved for release.
- [ ] Create and push tag `v0.4.0` only after the release merge.
- [ ] Publish GitHub Release notes from `docs/releases/v0.4.0.md`.
- [ ] Run PyPI readiness check before publishing.
- [ ] Publish to PyPI only when credentials and release approval are explicitly available.

## v0.4.0 Setup-Assistant Smoke Tests

- [x] Run  against a generated customer-service template.
- [x] Run .
- [x] Confirm golden demo outputs exist under .
- [x] Confirm README install wording does not claim PyPI availability before publish.
