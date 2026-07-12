# Dify Local RAG Starter

## Who This Is For

Developers who want to use Dify as the app/RAG layer while keeping the model runtime local and diagnosable.

## What It Builds

A reviewable plan for connecting Dify to a local OpenAI-compatible endpoint such as Ollama, vLLM, SGLang, LM Studio, or Xinference.

## Recommended Hardware

Dify itself can run on modest hardware. The model endpoint determines CPU, GPU, VRAM, and latency requirements.

## Commands

```bash
inferdoctor
inferdoctor check dify --endpoint http://127.0.0.1:5001
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor template show dify-rag
inferdoctor template compose dify-rag --output ./dify-rag-compose
```

## Validate

```bash
cd ./dify-rag-compose
cp .env.example .env
inferdoctor
```

## Troubleshooting

- If Dify is unreachable, verify its port and service status outside InferDoctor.
- If model calls fail, diagnose the model endpoint first with `inferdoctor check vllm` or `inferdoctor check sglang`.
- If `/v1/models` returns 404, verify whether the base URL should include `/v1`.

## Limitations

InferDoctor does not install Dify, start containers, create Dify apps, download models, or run inference. Generated Compose files are optional review aids.
