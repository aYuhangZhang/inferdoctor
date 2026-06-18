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
