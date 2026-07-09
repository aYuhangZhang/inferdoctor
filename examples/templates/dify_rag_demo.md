# Dify RAG Demo

## Goal

Use Dify as the RAG/app layer while keeping the local model endpoint diagnosable.

## Commands

```bash
inferdoctor
inferdoctor template show dify-rag
inferdoctor template compose dify-rag --output ./dify-rag-compose
inferdoctor check dify --endpoint http://127.0.0.1:5001
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
```

## Generated Files

- `docker-compose.yml`
- `.env.example`
- `config.yaml`
- `README.md`

## Validation

Review generated Compose files manually. InferDoctor does not start Dify or pull images.

## Next Steps

Configure Dify to use your local OpenAI-compatible endpoint, then diagnose endpoint failures with InferDoctor.

## Limitations

This is setup guidance only. It does not install Dify, create Dify apps, download models, or run inference.
