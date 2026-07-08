# InferDoctor v0.2 Launch Post Draft

Diagnose your local AI stack in one command.

InferDoctor is an open-source diagnostic CLI for developers running local AI
inference stacks. It helps answer the question developers hit constantly:

Why doesn't my local AI stack work?

```bash
inferdoctor
```

It checks the machine, NVIDIA driver, CUDA toolkit, Ollama, vLLM, SGLang,
Xinference, Dify, and OpenAI-compatible endpoints. The output is designed to be
screenshot-friendly: health score, component table, and top recommended fixes.

New in the v0.2 development branch:

- screenshot-friendly local AI stack health dashboard;
- Top Fixes with likely cause, impact, command, and config hint;
- OpenAI-compatible endpoint diagnostics for vLLM and SGLang;
- `inferdoctor explain <topic>` troubleshooting guides;
- `inferdoctor capacity` lightweight hardware readiness preview;
- JSON and Markdown reports for sharing diagnostics.

InferDoctor does not install runtimes, download models, run inference, or modify
system settings. It is read-only by default and safe on CPU-only machines.

Model recommendation tools help you choose a model. InferDoctor helps you find
why the stack that should run the model is broken.

Install: `pip install inferdoctor`

Repository: https://github.com/anguoyang/inferdoctor
