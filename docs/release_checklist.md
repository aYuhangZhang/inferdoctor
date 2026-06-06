# v0.1.0 Release Checklist

## Code and Compatibility

- [ ] Version is `0.1.0` in package metadata and `inferdoctor.__version__`.
- [ ] Runtime dependencies remain empty or lightweight and justified.
- [ ] All checks run safely on a CPU-only machine.
- [ ] Missing GPU tools and inference services do not crash the CLI.
- [ ] `inferdoctor check --help` documents supported options.
- [ ] JSON and Markdown report formats are valid and contain no secrets.

## Validation

- [ ] Run `python -m pip install -e ".[dev]"`.
- [ ] Run `inferdoctor check`.
- [ ] Run `inferdoctor report --format json`.
- [ ] Run `inferdoctor report --format markdown`.
- [ ] Run `pytest`.
- [ ] Run `git diff --check`.
- [ ] Confirm GitHub Actions passes on all configured Python versions.

## Documentation and Governance

- [ ] README installation, quick start, status semantics, and examples are current.
- [ ] CPU-only sample reports are sanitized.
- [ ] `CONTRIBUTING.md` reflects the checker architecture and test requirements.
- [ ] `SECURITY.md` points to a private reporting channel.
- [ ] Bug and feature issue templates are available.
- [ ] Apache License 2.0 remains present.

## GitHub Release

- [ ] Review the final commit on `main`.
- [ ] Create annotated tag `v0.1.0`.
- [ ] Push the tag.
- [ ] Create a GitHub release with highlights, supported checks, and limitations.
- [ ] Verify the CI badge and release links from a logged-out browser.
