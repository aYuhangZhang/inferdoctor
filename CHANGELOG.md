# Changelog

## Unreleased / v0.2.0

### Highlights

- Screenshot-friendly default health dashboard for `inferdoctor`.
- Heuristic overall health score and stack summary.
- Top Fixes with likely cause, impact, next command, and config hint.
- Reusable OpenAI-compatible endpoint diagnostics for `/v1/models`.
- First-class SGLang checker.
- Improved vLLM, Xinference, Dify, CUDA, NVIDIA, and HTTP failure suggestions.
- `inferdoctor explain <topic>` troubleshooting guides for common local AI failures.
- `inferdoctor capacity` lightweight local AI hardware readiness preview.
- Updated README, console examples, launch post draft, and release checklist.

### Safety

- No heavy AI runtime dependencies were added.
- No model download or inference execution features were added.
- Diagnostics remain lightweight and read-only by default.
- Tests continue to use mocks and do not require GPU, CUDA, local runtimes, or internet access.
