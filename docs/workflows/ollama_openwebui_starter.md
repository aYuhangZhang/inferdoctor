# Ollama + Open WebUI Starter

## Who This Is For

Users who want the easiest local chat path: Ollama as the model backend and Open WebUI as the browser interface.

## What It Builds

A diagnosis-first setup flow. InferDoctor checks whether Ollama and Open WebUI are reachable and shows optional Compose guidance for Open WebUI.

## Commands

```bash
inferdoctor
inferdoctor check ollama --endpoint http://127.0.0.1:11434
inferdoctor check openwebui --endpoint http://127.0.0.1:3000
inferdoctor template compose open-webui --output ./open-webui-compose
```

## Suggested Flow

1. Confirm Ollama is running and reachable.
2. Confirm Open WebUI is reachable.
3. Configure Open WebUI to point at the Ollama/OpenAI-compatible endpoint.
4. Use InferDoctor again when the UI or backend fails.

## Limitations

InferDoctor does not install Ollama, download models, pull Open WebUI images, start containers, or run inference.
