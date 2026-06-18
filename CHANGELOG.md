# Changelog

## Unreleased / v0.4.0

### Highlights

- Beginner setup journeys polished across diagnosis, recommendation, stack planning, bootstrap dry-run, template creation, validation, and smoke testing.
- Generated starter apps now make dry-run and config-check paths clearer before any live model endpoint is used.
- `inferdoctor template smoke-test` support is emphasized in recommended next steps and generated project flow.
- Golden demo outputs added for health check, capacity, recommendations, stack plan, bootstrap dry-run, template validation, template smoke-test, and model fit.
- README first screen updated around the setup-assistant workflow.
- v0.4.0 release notes drafted for a future public release.

### Safety

- No heavy AI runtime dependencies were added.
- No model download or model execution commands were added.
- Template smoke tests remain read-only and do not call endpoints.
- Stack bootstrap remains dry-run guidance, not an installer.
- Recommendations and model-fit estimates remain heuristics, not benchmarks.

## v0.3.0

### Highlights

- Template catalog for common local AI app goals.
- Starter project generation for customer service, restaurant ordering, and local document Q&A demos.
- Guided `inferdoctor init` setup path.
- Hardware-aware `inferdoctor recommend` stack recommendations.
- Heuristic `inferdoctor model fit` advisor.
- Improved generated starter templates with local endpoint config and troubleshooting.
- Beginner documentation for getting started, templates, recommendations, model fit, and local AI concepts.
- Public v0.3.0 release readiness checks and install smoke test coverage.

### Safety

- No heavy AI runtime dependencies were added.
- No model download or model execution commands were added.
- Template generation writes only to the explicit output directory.
- Recommendations and model-fit estimates remain heuristics, not benchmarks.

## v0.2.0

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
