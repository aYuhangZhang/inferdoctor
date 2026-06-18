# Restaurant Ordering Template Demo

Use this when you want a concrete chatbot scenario with menu data, ordering policy, and safe local endpoint configuration.

## Command

```bash
inferdoctor template create restaurant-ordering --output ./restaurant-ordering-demo
inferdoctor template validate ./restaurant-ordering-demo
```

## Generated Files

- `README.md`
- `app.py`
- `requirements.txt`
- `.env.example`
- `config.yaml`
- `prompts/system_prompt.md`
- `data/menu.yaml`
- `data/policies.md`
- `examples/sample_orders.md`
- `troubleshooting.md`

## Connect a Local Endpoint

Use `.env` for the local OpenAI-compatible endpoint:

```bash
LOCAL_AI_BASE_URL=http://127.0.0.1:1234/v1
LOCAL_AI_MODEL=local-model
```

LM Studio is often convenient for demos. vLLM and SGLang are better fits when you want a local API server on a GPU machine.

## What It Solves

This template gives a realistic menu assistant that asks about pickup, spice level, allergies, and order confirmation.

## Validate

```bash
inferdoctor template validate ./restaurant-ordering-demo
```
