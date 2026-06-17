# InferDoctor Release Report

## Release

- Version: `v0.2.0`
- Main release commit: `a5f6b947ea2eed9f8c54ede76253df2a44758251`
- Dev commit after merging release back: `dd6430540e0cc1c6877e4ddbd24584a645ab2aed`
- Tag commit: `a5f6b947ea2eed9f8c54ede76253df2a44758251`
- Tag: `v0.2.0`

## Tests Run

On `dev` before release:

- `pytest`: `47 passed`
- `inferdoctor`
- `inferdoctor check sglang`
- `inferdoctor capacity`
- `inferdoctor explain openai-compatible-404`

On `main` after merge:

- `pytest`: `47 passed`

## GitHub Actions

- Main release workflow: https://github.com/anguoyang/inferdoctor/actions/runs/27722148589
- Tag workflow: https://github.com/anguoyang/inferdoctor/actions/runs/27722163022

## Release Highlights

- Screenshot-friendly local AI stack health dashboard.
- Heuristic overall health score and stack summary.
- Top Fixes with likely cause, impact, command, and config hint.
- OpenAI-compatible endpoint diagnostics for vLLM and SGLang.
- First-class SGLang checker.
- `inferdoctor explain <topic>` troubleshooting guides.
- `inferdoctor capacity` lightweight hardware readiness preview.
- README, examples, launch post draft, changelog, and release checklist polish.

## Next Step

Create GitHub Release notes for `v0.2.0` if they are not automated.
