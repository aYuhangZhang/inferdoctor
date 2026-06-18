# Customer Service Template Demo

Use this when you want a small local FAQ assistant without adding a vector database yet.

## Command

```bash
inferdoctor template create customer-service --output ./customer-service-demo
inferdoctor template validate ./customer-service-demo
```

## Generated Files

- `README.md`
- `app.py`
- `requirements.txt`
- `.env.example`
- `config.yaml`
- `prompts/system_prompt.md`
- `data/faq.md`
- `troubleshooting.md`

## Connect a Local Endpoint

Edit `.env` or `config.yaml`:

```bash
LOCAL_AI_BASE_URL=http://127.0.0.1:8000/v1
LOCAL_AI_MODEL=local-model
```

Common local endpoint examples:

- Ollama OpenAI-compatible: `http://127.0.0.1:11434/v1`
- LM Studio: `http://127.0.0.1:1234/v1`
- vLLM: `http://127.0.0.1:8000/v1`
- SGLang: `http://127.0.0.1:30000/v1`

## What It Solves

A beginner can test a local support chatbot using realistic FAQ data and a local OpenAI-compatible endpoint.

## Validate

```bash
inferdoctor template validate ./customer-service-demo
```
