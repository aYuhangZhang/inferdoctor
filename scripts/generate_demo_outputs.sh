#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
EXAMPLES="$ROOT/examples"
mkdir -p "$EXAMPLES"

cat > "$EXAMPLES/demo_health_dashboard.txt" <<'EOF'
InferDoctor - Local AI Stack Health Check
=========================================================
Overall Health: 82 / 100  (Mostly healthy)
Stack Summary: 3 working | 2 needs attention | 3 optional/offline | 0 failed
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
Dify        WARN     Dify responded with HTTP 502

Top recommended fixes (most useful first):
1. vLLM: vLLM models route returned HTTP 404
   Likely cause: The service responded, but /v1/models was not found. The base URL may be missing or duplicating /v1.
   Impact: Needs attention if your app depends on vLLM.
   Try: inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
   Config: endpoints.vllm: http://127.0.0.1:8000/v1
2. Dify: Dify responded with HTTP 502
   Likely cause: Dify is optional. If you run it locally, the service may be stopped or mapped to another port.
   Impact: Needs attention if your app depends on Dify.
   Try: inferdoctor check dify --endpoint http://127.0.0.1:5001
   Config: endpoints.dify: http://127.0.0.1:5001
EOF

cat > "$EXAMPLES/demo_top_fixes.txt" <<'EOF'
Top recommended fixes (most useful first):
1. SGLang: SGLang endpoint is not reachable
   Likely cause: The service may not be running, or it may be listening on another port.
   Impact: Optional unless SGLang is part of your local stack.
   Try: inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
   Config: endpoints.sglang: http://127.0.0.1:30000/v1

2. CUDA: CUDA compiler was not found
   Likely cause: NVIDIA driver is available, but CUDA toolkit was not found. This may be OK if you only use prebuilt runtimes such as Ollama.
   Impact: Optional for CPU-only and many prebuilt runtimes; required for CUDA compilation.
   Try: nvcc --version
   Note: Install CUDA toolkit only if you need to compile CUDA workloads or use runtimes that require nvcc.

3. Dify: Dify endpoint is not reachable
   Likely cause: Dify is optional. If you run it locally, the service may be stopped or mapped to another port.
   Impact: Optional unless Dify is part of your local stack.
   Try: inferdoctor check dify --endpoint http://127.0.0.1:5001
   Config: endpoints.dify: http://127.0.0.1:5001
EOF

cat > "$EXAMPLES/demo_capacity.txt" <<'EOF'
InferDoctor Capacity Preview
=========================================================
Detected GPU: Example NVIDIA RTX 3090
Detected VRAM: 24.0 GiB

This is a rough planning heuristic, not a benchmark.
InferDoctor does not download models or run inference.

Workload class             Readiness     Notes
-------------------------  ------------  ------------------------------------
Small local chat           Likely OK      7B-class quantized models are realistic.
Medium local chat          Likely OK      14B-class quantized models may fit.
Large local chat           Needs care     32B-class workloads depend on quantization and context.
High-throughput serving    Needs care     Validate runtime, batching, and KV cache behavior.
EOF

cat > "$EXAMPLES/demo_explain.txt" <<'EOF'
InferDoctor Explain: OpenAI-compatible endpoint returned 404
============================================================

What it means:
The server responded, but the route InferDoctor checked was not found.

Common causes:
- The endpoint is missing the /v1 prefix.
- The server exposes a web UI but not an OpenAI-compatible API.
- A reverse proxy is routing /v1/models incorrectly.

What to try next:
- Try adding /v1 to the configured endpoint.
- Check whether /v1/models exists in the runtime logs.
- Retry the component check with --endpoint.

Related command:
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
EOF

cat > "$EXAMPLES/demo_scenarios.txt" <<'EOF'
InferDoctor Scenario Readiness
=========================================================
Goal-oriented diagnosis for common local AI setups.

Local chatbot:
  Status: PASS
  Reason: Ollama is available, so a local chatbot path is ready.
  Next step: Run inferdoctor check ollama if chat requests still fail.

RAG app:
  Status: WARN
  Reason: A model endpoint is available, but Dify or embedding infrastructure was not confirmed.
  Next step: Configure Dify or verify your embedding endpoint and vector database.

OpenAI-compatible server:
  Status: WARN
  Reason: A server responded, but the OpenAI-compatible models route needs attention.
  Next step: Run inferdoctor explain openai-compatible-404 or retry with --endpoint.

GPU inference:
  Status: PASS
  Reason: NVIDIA GPU is visible; CUDA toolkit may be optional for prebuilt runtimes.
  Next step: Use inferdoctor capacity for rough workload readiness estimates.
EOF

cat > "$EXAMPLES/demo_profile.md" <<'EOF'
# InferDoctor Safe Diagnostic Profile

Generated: `2026-06-18T00:00:00+00:00`

> Safe to share by default: secrets, endpoint credentials, query strings, and home paths are redacted.

## System

| Field | Value |
| --- | --- |
| os | Linux-example-x86_64 |
| python_version | 3.12.3 |
| architecture | x86_64 |
| available_memory_gib | 24.0 |

## GPUs

| GPU | VRAM | Driver |
| --- | --- | --- |
| NVIDIA GeForce RTX 3090 | 24.0 GiB | 580.159.03 |

## Commands

| Command | Available | Path |
| --- | --- | --- |
| nvcc | no | unknown |
| nvidia-smi | yes | /usr/bin/nvidia-smi |
| ollama | yes | /usr/local/bin/ollama |

## Configured Endpoints

| Name | URL |
| --- | --- |
| ollama | `http://127.0.0.1:11434` |
| vllm | `http://127.0.0.1:8000/v1` |
| sglang | `http://127.0.0.1:30000/v1` |

## Checker Summary

| Check | Status | Summary |
| --- | --- | --- |
| system | **PASS** | System information collected |
| nvidia | **PASS** | 1 NVIDIA GPU(s) detected |
| cuda | **SKIP** | CUDA compiler was not found |
| ollama | **PASS** | Ollama CLI and API are available |
| vllm | **WARN** | vLLM models route returned HTTP 404 |

## Top Fixes

1. **vLLM**: vLLM models route returned HTTP 404
   - Likely cause: The service responded, but /v1/models was not found. The base URL may be missing or duplicating /v1.
   - Try: `inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1`
EOF

printf 'Generated demo outputs in %s\n' "$EXAMPLES"
