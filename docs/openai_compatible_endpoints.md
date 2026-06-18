# OpenAI-Compatible Endpoints

An OpenAI-compatible endpoint is a local HTTP API that uses routes similar to the OpenAI API, usually under `/v1`.

## Common Routes

- `/v1/models` lists available models.
- `/v1/chat/completions` accepts chat messages.

## Common Local URLs

- Ollama OpenAI-compatible: `http://127.0.0.1:11434/v1`
- LM Studio: `http://127.0.0.1:1234/v1`
- vLLM: `http://127.0.0.1:8000/v1`
- SGLang: `http://127.0.0.1:30000/v1`
- Xinference OpenAI-compatible mode may be exposed under a `/v1` route depending on configuration.

## Common Errors

- Connection refused: the server is not running or the port is wrong.
- Timeout: the server is overloaded, blocked, or slow to load a model.
- 401 or 403: auth is required.
- 404: the base URL may be wrong, often missing `/v1`.
- Invalid JSON: the service is reachable but not speaking OpenAI-compatible JSON.

## Diagnose

```bash
inferdoctor check vllm --endpoint http://127.0.0.1:8000/v1
inferdoctor check sglang --endpoint http://127.0.0.1:30000/v1
inferdoctor explain openai-compatible-404
```
