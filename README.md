# InferDoctor

**Diagnose your local AI inference stack in one command.**

InferDoctor is an open-source diagnostic tool for local AI inference stacks. It
helps developers find why Ollama, vLLM, Xinference, Dify, CUDA, NVIDIA drivers,
and edge AI runtimes do not work as expected.

InferDoctor is deliberately lightweight, read-only by default, and safe to run
on machines without a GPU. It diagnoses existing environments without
installing or importing AI runtimes.

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

Generate machine-readable or shareable reports:

```bash
inferdoctor report --format json
inferdoctor report --format json --output report.json
inferdoctor report --format markdown --output report.md
```

## Example Output

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

`skip` is expected when an optional runtime or GPU tool is not present.
`warn` identifies a reachable but incomplete setup or an installed service that
is not running. `fail` is reserved for broken diagnostics or commands that are
present but report an error.

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
keeps the runtime dependency-free.

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
requests.

## Roadmap

- llama.cpp server and build diagnostics
- ONNX Runtime provider diagnostics
- TensorRT library and version diagnostics
- SGLang OpenAI-compatible endpoint checks
- Edge AI runtime checks for RKNN and other accelerators
- Optional discovery of common container and service configurations
- A stable third-party checker entry-point API

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE).
