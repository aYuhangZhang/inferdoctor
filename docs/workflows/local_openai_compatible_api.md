# Local OpenAI-Compatible API Workflow

## Who This Is For

Developers who want local apps to talk to vLLM, SGLang, LM Studio, llama.cpp server, Ollama, or Xinference through an OpenAI-compatible API.

## What It Builds

A diagnosis-first path for confirming the base URL, `/v1/models`, and chat completions compatibility.

## Recommended Hardware

CPU-only can test connectivity. GPU is usually needed for responsive serving of larger models.

## Runtime Options

- Easiest: LM Studio or Ollama OpenAI-compatible mode.
- Performance: vLLM or SGLang.
- CPU experiments: llama.cpp server.

## Commands

```bash
inferdoctor
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor check lmstudio --endpoint http://127.0.0.1:1234/v1
inferdoctor explain openai-compatible-404
```

## Validate

A healthy endpoint should usually respond on `/v1/models`. If a service responds with 404, try adding or removing `/v1` from the base URL.

## Limitations

InferDoctor checks endpoint shape. It does not start the runtime, download models, or run benchmark traffic.

## Next Upgrades

Add auth handling, reverse proxy checks, and app-specific request tests after the base endpoint is healthy.
