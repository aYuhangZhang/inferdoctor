# Ollama to Open WebUI Workflow

## Who This Is For

Beginners who want a browser chat UI backed by a local Ollama setup.

## What It Builds

A diagnosis path for checking Ollama, Open WebUI, Docker, and basic hardware readiness.

## Recommended Hardware

CPU-only can work with small models. NVIDIA GPU improves latency for supported setups.

## Runtime Options

- Ollama for local model serving.
- Open WebUI for browser chat.
- Docker if your Open WebUI installation uses containers.

## Commands

```bash
inferdoctor
inferdoctor check ollama
inferdoctor check openwebui --endpoint http://127.0.0.1:3000
inferdoctor check docker
inferdoctor capacity --vram 24 --model-size 14b --quant q4
```

## Validate

Ollama should respond on its API endpoint. Open WebUI should be reachable in the browser or by the endpoint check.

## Troubleshooting

```bash
inferdoctor explain openai-compatible-connection-refused
inferdoctor profile --format markdown
```

## Limitations

InferDoctor does not install Ollama, start Open WebUI, pull models, or start Docker containers.

## Next Upgrades

Add a browser setup checklist, Docker Compose examples, and a model/runtime fit advisor for common Open WebUI paths.
