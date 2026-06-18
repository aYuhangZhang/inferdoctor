# Open WebUI Local Chat Starter

## Who This Is For

Beginners who want a browser UI for local chat while using an existing local model backend.

## What It Builds

A safe setup path for diagnosing Open WebUI and its backend endpoint before running chat traffic.

## Runtime Options

- Ollama for the easiest local backend.
- LM Studio for a desktop OpenAI-compatible endpoint.
- vLLM or SGLang for GPU-oriented serving.

## Commands

```bash
inferdoctor
inferdoctor check openwebui --endpoint http://127.0.0.1:3000
inferdoctor template show open-webui
inferdoctor template compose open-webui --output ./open-webui-compose
```

## Validate

Review the generated `docker-compose.yml` manually before running Docker commands. InferDoctor does not start containers.

## Troubleshooting

- If Open WebUI loads but chat fails, diagnose the backend endpoint.
- If the backend is Ollama, check `inferdoctor check ollama`.
- If using vLLM/SGLang, check `/v1/models` with the matching checker.

## Limitations

InferDoctor does not install Open WebUI, pull images, start services, or run model inference.
