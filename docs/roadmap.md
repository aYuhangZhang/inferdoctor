# InferDoctor Roadmap

InferDoctor is evolving from a local AI stack checker into a local AI stack doctor and setup assistant.

The default behavior should remain lightweight, read-only, local-first, and beginner-friendly.

## Current Positioning

InferDoctor helps users answer:

1. Why does my local AI stack not work?
2. What can this machine realistically run?
3. What local AI app can I start building next?

## v0.4.0 Focus

v0.4.0 is focused on adoption and practical usefulness after the v0.3 setup-assistant milestone.

Planned focus areas:

- Template smoke tests for generated starter projects.
- Dry-run stack bootstrap plans.
- Real-world workflow docs for common local AI scenarios.
- Stronger use-case recommendations for hardware and model fit.
- Better demo outputs for screenshots and docs.
- Better beginner UX for template creation, validation, and endpoint configuration.
- More explicit safety messaging around what InferDoctor will not do automatically.

## v0.5.0 Possibilities

v0.5.0 may explore optional setup assistance, while keeping destructive or heavy actions opt-in.

Possible directions:

- Optional safe bootstrap execution for file generation and lightweight checks.
- More templates for local AI applications.
- Docker Compose generation for users who explicitly request it.
- Dify workflow templates.
- Open WebUI integration guide.
- Benchmark result import, not benchmark execution by default.
- Community template registry.
- Japanese enterprise RAG setup guide.

## Long-Term Direction

InferDoctor should help a beginner go from a fresh machine to a working local AI demo:

1. Diagnose the machine.
2. Understand hardware and runtime fit.
3. Pick a realistic stack.
4. Generate a starter template.
5. Validate and smoke-test the generated project.
6. Configure an existing local endpoint.
7. Run the demo.
8. Upgrade runtime, model, retrieval, or deployment later.

## Non-Goals

InferDoctor should not become a heavy runtime.

By default, it should not:

- install AI runtimes;
- download models;
- run real model inference;
- start services or containers;
- modify system settings;
- claim benchmark accuracy from heuristics.

Optional future bootstrap commands must clearly separate dry-run planning from actions that write files, install packages, or call endpoints.
