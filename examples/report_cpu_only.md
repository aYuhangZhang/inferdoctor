# InferDoctor Report

Generated: `2026-06-10T00:00:00+00:00`

| Check | Status | Summary |
| --- | --- | --- |
| system | **PASS** | System information collected |
| nvidia | **SKIP** | nvidia-smi was not found |
| cuda | **SKIP** | CUDA compiler was not found |
| ollama | **SKIP** | Ollama was not found and its API is not reachable |
| vllm | **SKIP** | vLLM endpoint is not reachable |
| sglang | **SKIP** | SGLang endpoint is not reachable |
| xinference | **SKIP** | Xinference endpoint is not reachable |
| dify | **SKIP** | Dify endpoint is not reachable |

## system

System information collected

**Details**

- OS: Linux-6.8.0-x86_64-with-glibc2.39
- Python: 3.12.3
- Architecture: x86_64
- Available memory: 7.8 GiB

## nvidia

nvidia-smi was not found

**Details**

- No NVIDIA management CLI is available on PATH.

**Suggestions**

- If this machine has an NVIDIA GPU, install or repair its driver.
- Skip this check on CPU-only or non-NVIDIA systems.

## cuda

CUDA compiler was not found

**Details**

- nvcc is not available on PATH.

**Suggestions**

- No action is needed for CPU-only inference or many prebuilt runtimes such as Ollama.
- Install CUDA toolkit only if you need nvcc for compilation or a runtime that requires it.

## ollama

Ollama was not found and its API is not reachable

**Details**

- http://127.0.0.1:11434/api/tags: Connection refused. The endpoint is not reachable; the service may not be running or may be listening on another port.

**Suggestions**

- Start Ollama or update endpoints.ollama.
- No action is needed if Ollama is not used on this machine.

## vllm

vLLM endpoint is not reachable

**Details**

- http://127.0.0.1:8000/v1/models: Connection refused. The endpoint is not reachable; the service may not be running or may be listening on another port.

**Suggestions**

- Start vLLM or verify endpoints.vllm.
- Retry with: inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1

## sglang

SGLang endpoint is not reachable

**Details**

- http://127.0.0.1:30000/v1/models: Connection refused. The endpoint is not reachable; the service may not be running or may be listening on another port.

**Suggestions**

- Start SGLang or verify endpoints.sglang.
- Retry with: inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1

## xinference

Xinference endpoint is not reachable

**Details**

- http://127.0.0.1:9997/v1/models: Connection refused. The endpoint is not reachable; the service may not be running or may be listening on another port.

**Suggestions**

- Start Xinference or update endpoints.xinference.
- Confirm the supervisor is listening on the configured host and port.
- No Xinference SDK is required for this check.

## dify

Dify endpoint is not reachable

**Details**

- http://127.0.0.1:5001/: Connection refused. The endpoint is not reachable; the service may not be running or may be listening on another port.

**Suggestions**

- Dify is optional. Add endpoints.dify to inferdoctor.yaml if you want to diagnose Dify connectivity.
- If Dify is running, check its service status and container port mappings.
