# InferDoctor

[![Tests](https://github.com/anguoyang/inferdoctor/actions/workflows/tests.yml/badge.svg)](https://github.com/anguoyang/inferdoctor/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](pyproject.toml)

**Diagnose your local AI stack in one command.**

Find out why Ollama, vLLM, SGLang, Xinference, Dify, CUDA, or your GPU setup is
not working. InferDoctor is the doctor for local AI inference stacks: it gives
you a screenshot-friendly health summary, top fixes, troubleshooting explainers,
and a rough capacity preview without installing or running AI runtimes.

```bash
inferdoctor
```

Model recommendation tools help you choose a model. InferDoctor helps you
understand why your local AI stack is broken.

## Example Output

```text
InferDoctor - Local AI Stack Health Check
=========================================================
Overall Health: 88 / 100  (Mostly healthy)
Stack Summary: 3 working | 1 needs attention | 4 optional/offline | 0 failed
Doctor's read: Some components need attention. Start with the first fix below.
PASS 100 | WARN 60 | FAIL 0 | SKIP 85  (heuristic)

Component   Status   Summary
----------- -------- --------------------------------------------------
System      PASS     System information collected
NVIDIA      PASS     1 NVIDIA GPU(s) detected
CUDA        SKIP     CUDA compiler was not found
Ollama      PASS     Ollama CLI and API are available
vLLM        WARN     vLLM models route returned HTTP 404
SGLang      SKIP     SGLang endpoint is not reachable
Xinference  SKIP     Xinference endpoint is not reachable
Dify        SKIP     Dify endpoint is not reachable

Top recommended fixes (most useful first):
1. vLLM: vLLM models route returned HTTP 404
   Likely cause: The service responded, but /v1/models was not found. The base URL may be missing or duplicating /v1.
   Impact: Needs attention if your app depends on vLLM.
   Try: inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
   Config: endpoints.vllm: http://127.0.0.1:8000/v1
```

More screenshot-friendly samples:

- [`examples/console_cpu_only.txt`](examples/console_cpu_only.txt)
- [`examples/console_with_ollama.txt`](examples/console_with_ollama.txt)
- [`examples/console_with_gpu.txt`](examples/console_with_gpu.txt)

## Diagnose, Don't Guess

Use the commands that match the question you have:

```bash
inferdoctor                              # health score, component table, top fixes
inferdoctor explain openai-compatible-404
inferdoctor capacity --vram 24
inferdoctor report --format markdown
```

InferDoctor does not choose models for you. It tells you whether the local stack
that should serve those models is actually healthy.

## Why InferDoctor?

A local AI request can fail because of the operating system, driver, CUDA
toolkit, runtime process, endpoint URL, authentication, reverse proxy, or API
response format. These failures often look identical from the application.

InferDoctor checks each layer separately and turns low-level symptoms into
short, practical next steps.

## One Command, One Answer

Running `inferdoctor` is the same as running `inferdoctor check`:

```bash
inferdoctor
```

The dashboard immediately shows:

- an overall health score;
- which components pass, warn, fail, or are optional and skipped;
- a short explanation for every component;
- the top three recommended fixes;
- exact commands and configuration hints to try next.

The score is a transparent heuristic, not a benchmark. `PASS` contributes 100,
`WARN` 60, `FAIL` 0, and optional `SKIP` results contribute 85 so an unused
runtime does not heavily penalize an otherwise healthy machine.

## What Problems Does InferDoctor Diagnose?

| Component | What InferDoctor checks |
| --- | --- |
| System | OS, Python version, CPU architecture, available memory |
| NVIDIA | `nvidia-smi`, driver version, GPU name, total VRAM |
| CUDA | `nvcc`, toolkit version, CUDA environment variables |
| Ollama | CLI discovery and `/api/tags` connectivity |
| vLLM | OpenAI-compatible `/v1/models` connectivity and response shape |
| SGLang | OpenAI-compatible `/v1/models` connectivity and response shape |
| Xinference | Supervisor endpoint connectivity without the SDK |
| Dify | Configurable Dify endpoint connectivity without the SDK |

OpenAI-compatible checks distinguish connection refusal, timeout, unauthorized
responses, wrong base URLs, invalid JSON, and non-compatible response shapes.

## Top Fixes

For the highest-priority problems, InferDoctor shows:

- the observed issue;
- the likely cause;
- whether the issue is optional or likely blocking;
- the next command to run;
- the relevant `inferdoctor.yaml` setting.

Example:

```text
1. SGLang: SGLang models route returned HTTP 404
   Likely cause: The service responded, but /v1/models was not found. The base URL may be missing or duplicating /v1.
   Impact: Needs attention if your app depends on SGLang.
   Try: inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
   Config: endpoints.sglang: http://127.0.0.1:30000/v1
```

## Quick Start

InferDoctor requires Python 3.9 or newer.

```bash
git clone https://github.com/anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e .
inferdoctor
```

Check one component or override its endpoint:

```bash
inferdoctor check nvidia
inferdoctor check ollama
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor check xinference
inferdoctor check dify
```

Show detailed raw diagnostic data or allow more time for remote endpoints:

```bash
inferdoctor check --verbose
inferdoctor check vllm --timeout 5
```

## Scenario Readiness

Use `inferdoctor scenario` when you want the answer framed around a goal instead
of a component:

```bash
inferdoctor scenario
inferdoctor scenario openai-compatible-server
```

Initial scenarios include local chatbot, RAG app, OpenAI-compatible server,
Dify local RAG, GPU inference, and CPU-only fallback. See
[`examples/scenario_readiness.txt`](examples/scenario_readiness.txt).

## Troubleshooting Explain

Use `inferdoctor explain` when you want a short, focused explanation for a
common local AI failure:

```bash
inferdoctor explain openai-compatible-404
inferdoctor explain cuda-toolkit-missing
inferdoctor explain vllm-endpoint-not-reachable
```

Each explanation includes what the symptom means, common causes, what to try
next, and the related InferDoctor command.

## Configuration

```yaml
endpoints:
  ollama: http://127.0.0.1:11434
  vllm: http://127.0.0.1:8000/v1
  sglang: http://127.0.0.1:30000/v1
  xinference: http://127.0.0.1:9997
  dify: http://127.0.0.1:5001
timeout: 2
```

```bash
inferdoctor check --config inferdoctor.yaml
```

The built-in YAML reader intentionally supports this small mapping format so
the runtime remains dependency-free. `--timeout` and `--endpoint` provide safe,
temporary overrides without editing configuration.

## Capacity Preview

Use `inferdoctor capacity` for a lightweight hardware readiness estimate:

```bash
inferdoctor capacity
inferdoctor capacity --vram 24
```

Capacity estimates are rough heuristics, not benchmarks. InferDoctor does not
download models, run inference, or recommend a model leaderboard.

## Reports

```bash
inferdoctor report --format json
inferdoctor report --format markdown
inferdoctor report --format json --output report.json
inferdoctor report --format markdown --output report.md
```

See the sanitized samples in
[`examples/report_cpu_only.json`](examples/report_cpu_only.json) and
[`examples/report_cpu_only.md`](examples/report_cpu_only.md).

## InferDoctor vs Model Recommendation Tools

| Question | Model recommendation tools | InferDoctor |
| --- | --- | --- |
| Which model should I use? | Yes | No |
| Why is my local endpoint failing? | Usually no | Yes |
| Is my NVIDIA driver visible? | Sometimes | Yes |
| Is `/v1/models` valid and compatible? | Usually no | Yes |
| Does it download or run models? | Sometimes | Never |

InferDoctor is not a model recommender. It does not choose, download, or run
models for you. It diagnoses the stack you already operate.

## What InferDoctor Does Not Do

- It does not install AI runtimes, drivers, CUDA packages, or models.
- It does not run inference or load model weights.
- It does not modify system settings or services.
- It does not require a GPU.
- It is read-only by default.

## Status Meaning

- `PASS`: the component responded as expected.
- `WARN`: the component is reachable or present, but needs attention.
- `FAIL`: a discovered component is broken or a diagnostic cannot complete.
- `SKIP`: an optional component is absent or offline; this is not automatically
  a system failure.

Only `FAIL` causes a non-zero diagnostic exit code.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

Tests use subprocess and HTTP mocks. They require no GPU, CUDA installation,
local inference runtime, or internet access.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).

## Roadmap

- richer capacity heuristics for more hardware profiles
- llama.cpp server and build diagnostics
- ONNX Runtime provider diagnostics
- TensorRT library and version diagnostics
- RKNN and other edge accelerator checks
- optional local container and service discovery
- stable third-party checker entry points
- richer report summaries without adding heavy runtime dependencies

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
