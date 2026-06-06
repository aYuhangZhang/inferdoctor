# InferDoctor

[![Tests](https://github.com/anguoyang/inferdoctor/actions/workflows/tests.yml/badge.svg)](https://github.com/anguoyang/inferdoctor/actions/workflows/tests.yml)

**Diagnose your local AI inference stack in one command.**

InferDoctor is an open-source diagnostic tool for local AI inference stacks. It
helps developers find why Ollama, vLLM, Xinference, Dify, CUDA, NVIDIA drivers,
and edge AI runtimes do not work as expected.

InferDoctor is deliberately lightweight, read-only by default, and safe to run
on machines without a GPU. It diagnoses existing environments without
installing or importing AI runtimes.

## What Problems Does InferDoctor Solve?

Local inference failures often cross several layers: the operating system, GPU
driver, CUDA toolkit, runtime process, HTTP endpoint, and application
configuration. InferDoctor provides one consistent diagnostic view across those
layers.

It helps answer questions such as:

- Is this machine CPU-only, or is an NVIDIA GPU visible to the driver?
- Does `nvidia-smi` work, and what driver and VRAM does it report?
- Is `nvcc` installed, and which CUDA toolkit version is active?
- Is Ollama installed but not running?
- Is an OpenAI-compatible vLLM endpoint reachable?
- Are Xinference or Dify listening at the configured URL?
- Can the results be shared as structured JSON or readable Markdown?

Missing optional runtimes do not crash the tool. They produce a diagnostic
status with a practical next step.

## What InferDoctor Does Not Do

- It does not install AI runtimes, drivers, CUDA packages, or models.
- It does not run inference or load model weights.
- It does not modify system settings, services, environment variables, or files.
- It is read-only by default and uses short subprocess and HTTP probes.

## Installation

InferDoctor requires Python 3.9 or newer.

```bash
git clone https://github.com/anguoyang/inferdoctor.git
cd inferdoctor
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

Run every built-in check:

```bash
inferdoctor check
```

Run one check:

```bash
inferdoctor check system
inferdoctor check nvidia
inferdoctor check cuda
inferdoctor check ollama
inferdoctor check vllm
inferdoctor check dify
inferdoctor check xinference
```

Show the structured raw data collected by each check:

```bash
inferdoctor check --verbose
```

Override the HTTP timeout for slow or remote services:

```bash
inferdoctor check --timeout 5
inferdoctor report --format markdown --timeout 5
```

Generate machine-readable or shareable reports:

```bash
inferdoctor report --format json
inferdoctor report --format json --output report.json
inferdoctor report --format markdown --output report.md
```

## Example Console Output

```text
[PASS] system     System information collected
       - OS: Linux-6.8.0-x86_64-with-glibc2.39
       - Python: 3.12.3
       - Architecture: x86_64
[SKIP] nvidia     nvidia-smi was not found
       suggestion: Skip this check on CPU-only or non-NVIDIA systems.
[WARN] ollama     Ollama is installed but its API is not reachable
       suggestion: Start Ollama or update endpoints.ollama.
```

Complete sanitized CPU-only examples are available in
[`examples/report_cpu_only.json`](examples/report_cpu_only.json) and
[`examples/report_cpu_only.md`](examples/report_cpu_only.md).

## JSON Report Example

```json
{
  "tool": "InferDoctor",
  "version": "0.1.0",
  "results": [
    {
      "name": "nvidia",
      "status": "skip",
      "summary": "nvidia-smi was not found",
      "details": ["No NVIDIA management CLI is available on PATH."],
      "suggestions": ["Skip this check on CPU-only or non-NVIDIA systems."],
      "raw_data": {"nvidia_smi_path": null}
    }
  ]
}
```

## Markdown Report Example

```markdown
| Check | Status | Summary |
| --- | --- | --- |
| system | **PASS** | System information collected |
| nvidia | **SKIP** | nvidia-smi was not found |
| ollama | **SKIP** | Ollama was not found and its API is not reachable |
```

## Why `skip`, `warn`, or `fail`?

- `skip`: an optional tool or service is absent. This is normal on CPU-only
  machines or when that runtime is not part of the local stack.
- `warn`: something is partially available or needs attention, such as an
  installed CLI whose service is offline or an endpoint requiring credentials.
- `fail`: a discovered component reports an error, or a checker itself cannot
  complete reliably. `fail` makes the command exit non-zero.

`pass` means the requested diagnostic completed and found the expected
component or response.

## Configuration

Pass a JSON file or a simple YAML file with endpoint overrides:

```bash
inferdoctor check --config inferdoctor.yaml
inferdoctor report --format markdown --config inferdoctor.yaml
```

Example `inferdoctor.yaml`:

```yaml
endpoints:
  ollama: http://127.0.0.1:11434
  xinference: http://127.0.0.1:9997
  vllm: http://127.0.0.1:8000/v1
  dify: http://127.0.0.1:5001
timeout: 2
```

The built-in YAML reader intentionally supports this small mapping format. This
keeps the runtime dependency-free. A CLI `--timeout` value takes precedence
over the configuration file.

## Supported Checks

| Check | Diagnostics |
| --- | --- |
| `system` | OS, Python version, CPU architecture, available memory |
| `nvidia` | `nvidia-smi`, driver version, GPU name, total VRAM |
| `cuda` | `nvcc`, CUDA toolkit version, CUDA environment variables |
| `ollama` | CLI discovery and `/api/tags` endpoint |
| `vllm` | OpenAI-compatible `/v1/models` endpoint |
| `xinference` | HTTP `/v1/models` endpoint without the SDK |
| `dify` | Configurable Dify base endpoint without the SDK |

The checker registry is plugin-style: each checker implements one small
read-only interface and returns the same structured result:

```yaml
name: ollama
status: pass
summary: Ollama CLI and API are available
details: []
suggestions: []
raw_data: {}
```

## Design Principles

- Lightweight: no GPU frameworks or inference servers are dependencies.
- Safe: diagnostics are read-only and use short subprocess and HTTP timeouts.
- Portable: all checks degrade cleanly on CPU-only machines.
- Structured: console, JSON, and Markdown use the same result model.
- Extensible: new runtimes can be added as independent checker plugins.
- Testable: command and network behavior is covered with mocks.

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

Tests do not require a GPU, CUDA, local inference services, or internet access.
GitHub Actions runs them on supported Python versions for pushes and pull
requests. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

## Roadmap

- llama.cpp server and build diagnostics
- ONNX Runtime provider diagnostics
- TensorRT library and version diagnostics
- SGLang OpenAI-compatible endpoint checks
- Edge AI runtime checks for RKNN and other accelerators
- Optional discovery of common container and service configurations
- A stable third-party checker entry-point API

## Security

Please follow [SECURITY.md](SECURITY.md) when reporting a vulnerability. Do not
put secrets, access tokens, private endpoints, or sensitive diagnostic output in
a public issue.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
