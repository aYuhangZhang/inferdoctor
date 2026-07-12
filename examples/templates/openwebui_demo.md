# Open WebUI Demo

## Goal

Use Open WebUI as a browser interface for an existing local model backend.

## Commands

```bash
inferdoctor
inferdoctor template show open-webui
inferdoctor template compose open-webui --output ./open-webui-compose
inferdoctor check openwebui --endpoint http://127.0.0.1:3000
```

## Generated Files

- `docker-compose.yml`
- `.env.example`
- `config.yaml`
- `README.md`

## Validation

```bash
cd ./open-webui-compose
cp .env.example .env
inferdoctor
```

## Next Steps

Point Open WebUI at Ollama, LM Studio, vLLM, SGLang, or another local OpenAI-compatible endpoint.

## Limitations

InferDoctor does not pull images, start containers, install Open WebUI, or run model inference.
