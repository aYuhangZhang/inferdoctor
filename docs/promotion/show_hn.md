# Show HN Draft

Show HN: InferDoctor - diagnose your local AI stack and start building local AI apps

I built InferDoctor, a lightweight open-source CLI for diagnosing local AI inference stacks.

Local AI failures are often hard to read: CUDA, NVIDIA driver, Ollama, vLLM, SGLang, Dify, Open WebUI, Docker, wrong `/v1` URL, or endpoint response shape can all look like the same app-level error.

InferDoctor gives:

- one-command health dashboard
- Top Fixes
- OpenAI-compatible endpoint diagnostics
- capacity and model-fit heuristics
- stack recommendations
- starter templates
- template validation and smoke tests
- dry-run setup plans

It is read-only by default and does not install runtimes, download models, run inference, or modify system settings.

GitHub: https://github.com/anguoyang/inferdoctor
