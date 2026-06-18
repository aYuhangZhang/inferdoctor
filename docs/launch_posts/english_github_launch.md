# Launch Draft: InferDoctor v0.3 Development Branch

Local AI is powerful, but debugging the local stack is still painful.

A request can fail because Ollama is not running, vLLM has the wrong `/v1` base
URL, SGLang is listening on another port, Dify is behind a container mapping,
CUDA is missing, the NVIDIA driver is unhealthy, Docker is stopped, or the
endpoint is returning HTML instead of OpenAI-compatible JSON.

InferDoctor is an open-source diagnostic CLI for that problem.

```bash
inferdoctor
```

It gives one screenshot-friendly answer:

- local AI stack health score;
- PASS/WARN/FAIL/SKIP table for each component;
- Top Fixes with likely cause and next command;
- OpenAI-compatible endpoint diagnostics;
- `inferdoctor explain <topic>` troubleshooting guides;
- `inferdoctor scenario` readiness for common use cases;
- `inferdoctor profile` safe redacted diagnostic export;
- lightweight capacity heuristics without running models.

Supported checks include System, NVIDIA, CUDA, Ollama, vLLM, SGLang, llama.cpp
server, LM Studio, Xinference, Dify, Open WebUI, and Docker.

InferDoctor does not install runtimes, download models, run inference, benchmark
hardware, modify system settings, or choose a model for you. Model recommendation
tools help you choose a model. InferDoctor helps you understand why the stack
that should run it is broken.

Repository: https://github.com/anguoyang/inferdoctor
